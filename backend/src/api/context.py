"""
Unified Context API - Single endpoint for agent context retrieval

Replaces fragmented context retrieval with OpenRAG + LCI unified API.
Agents call this to get "perfect context" for any task.

Features:
- Combines OpenRAG (documents/knowledge) + LCI (code)
- Hybrid search with SQL filters + semantic search
- Automatic query expansion and reranking
- Context quality scoring

Author: KLM v2.3
Version: 2.3.0
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

from backend.src.services.openrag_service import OpenRAGService, OpenRAGConfig

logger = logging.getLogger(__name__)


class ContextSource(str, Enum):
    """Source types for context retrieval."""

    LYRICS = "lyrics"
    SESSIONS = "sessions"
    CODE = "code"
    KNOWLEDGE = "knowledge"


class ContextQuality(str, Enum):
    """Quality assessment of retrieved context."""

    PERFECT = "perfect"  # High relevance, complete info
    GOOD = "good"  # Relevant, some gaps
    PARTIAL = "partial"  # Some relevance, gaps exist
    POOR = "poor"  # Low relevance, missing info
    NONE = "none"  # No relevant context found


@dataclass
class ContextItem:
    """A single piece of retrieved context."""

    id: str
    source: ContextSource
    title: str
    content: str
    metadata: Dict[str, Any]
    relevance_score: float
    url: Optional[str] = None


@dataclass
class RetrievedContext:
    """Complete context retrieved for an agent query."""

    query: str
    items: List[ContextItem]
    total_items: int
    quality: ContextQuality
    search_performed: List[ContextSource]
    expanded_queries: List[str]
    retrieved_at: datetime
    elapsed_ms: int


@dataclass
class ContextRequest:
    """Request for context retrieval."""

    query: str
    agent_id: str
    task_type: Optional[str] = None
    filters: Optional[Dict[str, str]] = None
    include_sources: List[ContextSource] = field(
        default_factory=lambda: [ContextSource.LYRICS, ContextSource.SESSIONS]
    )
    require_quality: ContextQuality = ContextQuality.GOOD


@dataclass
class ContextResponse:
    """Response with retrieved context."""

    context: RetrievedContext
    success: bool
    message: str


class UnifiedContextAPI:
    """
    Unified Context API for KLM v2.3 agents.

    Provides single entry point for all context retrieval needs:
    - Knowledge base (lyrics, documents) via OpenRAG
    - Code via LCI
    - Agent sessions via OpenRAG
    """

    def __init__(self, openrag_config: Optional[OpenRAGConfig] = None):
        self.openrag = OpenRAGService(openrag_config)
        self.lci_available = self._check_lci()

    def _check_lci(self) -> bool:
        """Check if LCI is available for code search."""
        try:
            import subprocess

            result = subprocess.run(
                ["npx", "lci", "status"], capture_output=True, timeout=5
            )
            return result.returncode == 0
        except Exception:
            logger.warning("LCI not available, code search disabled")
            return False

    async def retrieve(self, request: ContextRequest) -> RetrievedContext:
        """
        Retrieve context for an agent query.

        This is the main entry point for agents needing context.

        Args:
            request: Context retrieval request

        Returns:
            RetrievedContext with all relevant items
        """
        import time

        start_time = time.time()

        all_items: List[ContextItem] = []
        expanded_queries = self.openrag.expand_query(request.query)

        for query in expanded_queries:
            if ContextSource.LYRICS in request.include_sources:
                lyrics_items = await self._search_lyrics(query, request.filters)
                all_items.extend(lyrics_items)

            if ContextSource.SESSIONS in request.include_sources:
                session_items = await self._search_sessions(query, request.agent_id)
                all_items.extend(session_items)

            if ContextSource.CODE in request.include_sources and self.lci_available:
                code_items = await self._search_code(query)
                all_items.extend(code_items)

        unique_items = self._deduplicate(all_items)
        reranked_items = self._rerank(request.query, unique_items)
        quality = self._assess_quality(reranked_items, request.require_quality)

        elapsed_ms = int((time.time() - start_time) * 1000)

        return RetrievedContext(
            query=request.query,
            items=reranked_items,
            total_items=len(reranked_items),
            quality=quality,
            search_performed=request.include_sources,
            expanded_queries=expanded_queries,
            retrieved_at=datetime.now(),
            elapsed_ms=elapsed_ms,
        )

    async def _search_lyrics(
        self, query: str, filters: Optional[Dict[str, str]]
    ) -> List[ContextItem]:
        """Search lyrics via OpenRAG."""
        try:
            results = await self.openrag.hybrid_search(
                query=query, filters=filters, include_sessions=False
            )

            return [
                ContextItem(
                    id=r.id,
                    source=ContextSource.LYRICS,
                    title=r.title,
                    content=r.content[:500],
                    metadata=r.metadata,
                    relevance_score=r.similarity,
                )
                for r in results
            ]
        except Exception as e:
            logger.error(f"Lyrics search failed: {e}")
            return []

    async def _search_sessions(
        self, query: str, agent_id: Optional[str]
    ) -> List[ContextItem]:
        """Search agent sessions via OpenRAG."""
        try:
            filters = {"agent_id": agent_id} if agent_id else None
            results = await self.openrag.hybrid_search(
                query=query, filters=filters, include_lyrics=False
            )

            return [
                ContextItem(
                    id=r.id,
                    source=ContextSource.SESSIONS,
                    title=f"Session: {r.metadata.get('task_description', 'Unknown')}",
                    content=r.metadata.get("summary", "")[:500],
                    metadata=r.metadata,
                    relevance_score=r.similarity,
                )
                for r in results
            ]
        except Exception as e:
            logger.error(f"Session search failed: {e}")
            return []

    async def _search_code(self, query: str) -> List[ContextItem]:
        """Search code via LCI."""
        try:
            import subprocess

            result = subprocess.run(
                ["npx", "lci", "search", query],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                return []

            lines = result.stdout.strip().split("\n")
            return [
                ContextItem(
                    id=f"code_{i}",
                    source=ContextSource.CODE,
                    title=f"Code match: {line[:50]}" if line else "Code match",
                    content=line,
                    metadata={"source": "lci"},
                    relevance_score=0.7,
                )
                for i, line in enumerate(lines[:10])
                if line
            ]
        except Exception as e:
            logger.error(f"Code search failed: {e}")
            return []

    def _deduplicate(self, items: List[ContextItem]) -> List[ContextItem]:
        """Remove duplicate items by ID."""
        seen = set()
        unique = []
        for item in items:
            if item.id not in seen:
                seen.add(item.id)
                unique.append(item)
        return unique

    def _rerank(self, query: str, items: List[ContextItem]) -> List[ContextItem]:
        """Rerank items by true relevance."""

        def relevance_score(item: ContextItem) -> float:
            base = item.relevance_score
            quality_bonus = 0.1 if len(item.content) > 200 else 0.0
            return base + quality_bonus

        return sorted(items, key=relevance_score, reverse=True)

    def _assess_quality(
        self, items: List[ContextItem], required: ContextQuality
    ) -> ContextQuality:
        """Assess the quality of retrieved context."""
        if not items:
            return ContextQuality.NONE

        avg_relevance = sum(i.relevance_score for i in items) / len(items)
        has_content = all(len(i.content) > 50 for i in items)

        if avg_relevance > 0.85 and has_content:
            return ContextQuality.PERFECT
        elif avg_relevance > 0.7 and has_content:
            return ContextQuality.GOOD
        elif avg_relevance > 0.5:
            return ContextQuality.PARTIAL
        else:
            return ContextQuality.POOR


def create_context_api() -> FastAPI:
    """Create FastAPI app for Unified Context API."""
    app = FastAPI(
        title="KLM v2.3 Unified Context API",
        description="Single endpoint for agent context retrieval",
        version="2.3.0",
    )

    context_api = UnifiedContextAPI()

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        openrag_health = await context_api.openrag.get_health()
        return {
            "status": "healthy",
            "openrag": openrag_health,
            "lci": context_api.lci_available,
        }

    @app.post("/context/retrieve")
    async def retrieve_context(request: ContextRequest) -> ContextResponse:
        """
        Retrieve context for an agent query.

        Example:
        ```json
        {
            "query": "Ros Serey Sothea love songs",
            "agent_id": "AGT-002",
            "filters": {"era": "1960s"},
            "include_sources": ["lyrics", "sessions"]
        }
        ```
        """
        try:
            context = await context_api.retrieve(request)
            return ContextResponse(
                context=context,
                success=True,
                message=f"Retrieved {context.total_items} context items",
            )
        except Exception as e:
            logger.error(f"Context retrieval failed: {e}")
            raise HTTPException(
                status_code=500, detail=f"Context retrieval failed: {str(e)}"
            )

    @app.get("/context/sources")
    async def list_sources() -> Dict[str, Any]:
        """List available context sources."""
        return {
            "sources": [
                {
                    "name": "lyrics",
                    "description": "Khmer lyrics with embeddings",
                    "enabled": True,
                },
                {
                    "name": "sessions",
                    "description": "Agent session memory",
                    "enabled": True,
                },
                {
                    "name": "code",
                    "description": "Codebase semantic search (LCI)",
                    "enabled": context_api.lci_available,
                },
            ]
        }

    return app


def get_context_for_agent(
    query: str, agent_id: str, task_type: Optional[str] = None
) -> RetrievedContext:
    """
    Convenience function for getting agent context.

    Usage:
        context = get_context_for_agent(
            query="How to implement Romanization?",
            agent_id="AGT-002"
        )
    """
    import asyncio

    api = UnifiedContextAPI()
    request = ContextRequest(query=query, agent_id=agent_id, task_type=task_type)
    return asyncio.run(api.retrieve(request))
