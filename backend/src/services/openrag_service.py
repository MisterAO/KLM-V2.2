"""
OpenRAG Service - Unified Retrieval Layer for KLM v2.3

Provides:
- Hybrid search (SQL + semantic vector search)
- Query expansion for better recall
- Result reranking for precision
- Zero data drift architecture

Author: KLM v2.3
Version: 2.3.0
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

try:
    from supabase import create_client, Client
except ImportError:
    Client = None
    create_client = None

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Represents a search result with metadata."""

    id: str
    title: str
    content: str
    metadata: Dict[str, Any]
    similarity: float
    source: str


@dataclass
class IngestionResult:
    """Result of content ingestion."""

    id: str
    status: str
    embedding_generated: bool
    stored_at: datetime


class OpenRAGConfig:
    """Configuration for OpenRAG service."""

    def __init__(
        self,
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None,
        embedding_model: str = "text-embedding-3-large",
        embedding_dimensions: int = 1536,
        openrag_api_url: Optional[str] = None,
        openrag_api_key: Optional[str] = None,
        match_threshold: float = 0.7,
        match_count: int = 20,
        rerank_top_k: int = 5,
        enable_query_expansion: bool = True,
        expansion_max_terms: int = 5,
    ):
        self.supabase_url = supabase_url or os.getenv("SUPABASE_URL")
        self.supabase_key = supabase_key or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.embedding_model = embedding_model
        self.embedding_dimensions = embedding_dimensions
        self.openrag_api_url = openrag_api_url or os.getenv("OPENRAG_API_URL")
        self.openrag_api_key = openrag_api_key or os.getenv("OPENRAG_API_KEY")
        self.match_threshold = match_threshold
        self.match_count = match_count
        self.rerank_top_k = rerank_top_k
        self.enable_query_expansion = enable_query_expansion
        self.expansion_max_terms = expansion_max_terms


class OpenRAGService:
    """
    OpenRAG Service - Unified Retrieval for KLM v2.3

    Replaces ChromaDB placeholder with Supabase + OpenRAG architecture.
    Provides hybrid search combining SQL filtering with semantic vector search.
    """

    def __init__(self, config: Optional[OpenRAGConfig] = None):
        self.config = config or OpenRAGConfig()
        self._client: Optional[Client] = None
        self._connected = False

    def connect(self) -> bool:
        """Establish connection to Supabase."""
        if not create_client:
            logger.error("Supabase client not installed. Run: pip install supabase")
            return False

        if not self.config.supabase_url or not self.config.supabase_key:
            logger.error("Supabase URL and key not configured")
            return False

        try:
            self._client = create_client(
                self.config.supabase_url, self.config.supabase_key
            )
            self._connected = True
            logger.info("Connected to Supabase successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {e}")
            return False

    @property
    def client(self) -> Client:
        """Get Supabase client, connecting if necessary."""
        if not self._connected:
            if not self.connect():
                raise RuntimeError("Not connected to Supabase")
        return self._client

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI or OpenRAG.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding
        """
        try:
            if self.config.openrag_api_url:
                return await self._generate_openrag_embedding(text)
            else:
                return await self._generate_openai_embedding(text)
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise

    async def _generate_openai_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI API."""
        try:
            from openai import OpenAI
        except ImportError:
            logger.error("OpenAI client not installed. Run: pip install openai")
            raise

        client = OpenAI()
        response = client.embeddings.create(
            model=self.config.embedding_model,
            dimensions=self.config.embedding_dimensions,
            input=text,
        )
        return response.data[0].embedding

    async def _generate_openrag_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenRAG API."""
        import httpx

        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                f"{self.config.openrag_api_url}/embed",
                json={"text": text, "model": self.config.embedding_model},
                headers={"Authorization": f"Bearer {self.config.openrag_api_key}"},
            )
            response.raise_for_status()
            return response.json()["embedding"]

    def expand_query(self, query: str) -> List[str]:
        """
        Expand query with related terms for better recall.

        Uses simple synonym expansion. In production, could use
        OpenRAG's advanced query expansion.

        Args:
            query: Original search query

        Returns:
            List of expanded queries including original
        """
        if not self.config.enable_query_expansion:
            return [query]

        expansions = [query]

        khmer_related = {
            "love": ["romance", "heart", "feeling", "miss"],
            "home": ["family", "mother", "father", "country", "village"],
            "sad": ["lonely", "missing", "cry", "tears", "pain"],
            "happy": ["joy", "celebrate", "laugh", "smile"],
            "song": ["lyrics", "music", "melody", "voice"],
            "river": ["water", "flow", "current", " Mekong"],
            "moon": ["night", "sky", "stars", "light"],
        }

        query_lower = query.lower()
        for word, related in khmer_related.items():
            if word in query_lower:
                expansions.extend(related)

        return list(set(expansions))[: self.config.expansion_max_terms + 1]

    def rerank_results(
        self, query: str, results: List[Dict], top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Rerank search results using OpenRAG reranking.

        Reorders results by true relevance to the query,
        not just vector similarity.

        Args:
            query: Original query
            results: Raw search results
            top_k: Number of top results to return

        Returns:
            Reranked results
        """
        if top_k is None:
            top_k = self.config.rerank_top_k

        if not results:
            return []

        def calculate_relevance(result: Dict) -> float:
            """Calculate relevance score combining similarity with other factors."""
            similarity = result.get("similarity", 0.0)

            recency_bonus = 0.0
            if result.get("created_at"):
                try:
                    created = datetime.fromisoformat(
                        result["created_at"].replace("Z", "+00:00")
                    )
                    days_old = (datetime.now() - created).days
                    recency_bonus = max(0, 0.1 - (days_old / 365))
                except Exception:
                    pass

            completeness_bonus = 0.0
            if result.get("lyrics_khmer") and result.get("lyrics_english"):
                completeness_bonus = 0.05

            return similarity + recency_bonus + completeness_bonus

        reranked = sorted(results, key=calculate_relevance, reverse=True)
        return reranked[:top_k]

    async def hybrid_search(
        self,
        query: str,
        filters: Optional[Dict[str, str]] = None,
        include_lyrics: bool = True,
        include_sessions: bool = True,
    ) -> List[SearchResult]:
        """
        Perform hybrid search combining SQL filters with vector similarity.

        This is the core OpenRAG capability - combining structured
        filtering with semantic search for precise results.

        Args:
            query: Search query (will be expanded)
            filters: SQL filters (e.g., {"artist": "Ros Serey Sothea"})
            include_lyrics: Search lyrics table
            include_sessions: Search agent sessions

        Returns:
            List of SearchResult objects sorted by relevance
        """
        expanded_queries = self.expand_query(query)
        all_results: List[Dict] = []

        for expanded_query in expanded_queries:
            query_embedding = await self.generate_embedding(expanded_query)

            if include_lyrics:
                lyrics_results = await self._search_lyrics(query_embedding, filters)
                all_results.extend(lyrics_results)

            if include_sessions:
                session_results = await self._search_sessions(query_embedding, filters)
                all_results.extend(session_results)

        unique_results = self._deduplicate_results(all_results)
        reranked = self.rerank_results(query, unique_results)

        return [
            SearchResult(
                id=r["id"],
                title=r.get("title", r.get("task_description", "Unknown")),
                content=r.get("lyrics_khmer", r.get("summary", "")),
                metadata=r,
                similarity=r["similarity"],
                source=r.get("source", "unknown"),
            )
            for r in reranked
        ]

    async def _search_lyrics(
        self, embedding: List[float], filters: Optional[Dict[str, str]]
    ) -> List[Dict]:
        """Search lyrics table using hybrid_search_lyrics function."""
        try:
            result = self.client.rpc(
                "hybrid_search_lyrics",
                {
                    "query_embedding": embedding,
                    "match_threshold": self.config.match_threshold,
                    "match_count": self.config.match_count,
                    "filter_artist": filters.get("artist") if filters else None,
                    "filter_era": filters.get("era") if filters else None,
                    "filter_status": filters.get("status") if filters else None,
                },
            ).execute()

            return [{**row, "source": "lyrics"} for row in (result.data or [])]
        except Exception as e:
            logger.error(f"Lyrics search failed: {e}")
            return []

    async def _search_sessions(
        self, embedding: List[float], filters: Optional[Dict[str, str]]
    ) -> List[Dict]:
        """Search agent sessions table."""
        try:
            result = self.client.rpc(
                "search_similar_sessions",
                {
                    "query_embedding": embedding,
                    "match_threshold": self.config.match_threshold,
                    "match_count": self.config.match_count,
                    "agent_filter": filters.get("agent_id") if filters else None,
                },
            ).execute()

            return [{**row, "source": "sessions"} for row in (result.data or [])]
        except Exception as e:
            logger.error(f"Session search failed: {e}")
            return []

    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate results by ID."""
        seen = set()
        unique = []
        for r in results:
            if r["id"] not in seen:
                seen.add(r["id"])
                unique.append(r)
        return unique

    async def ingest_lyrics(
        self, lyrics_data: Dict[str, Any], embedding: Optional[List[float]] = None
    ) -> IngestionResult:
        """
        Ingest lyrics into Supabase with vector embedding.

        Zero data drift - metadata and embedding in same transaction.

        Args:
            lyrics_data: Lyrics metadata and content
            embedding: Pre-generated embedding (generated if not provided)

        Returns:
            IngestionResult with ID and status
        """
        text_for_embedding = (
            f"{lyrics_data.get('title', '')} {lyrics_data.get('lyrics_khmer', '')}"
        )

        if embedding is None:
            embedding = await self.generate_embedding(text_for_embedding)

        try:
            result = (
                self.client.table("lyrics")
                .insert({**lyrics_data, "embedding": embedding, "status": "processing"})
                .execute()
            )

            record = result.data[0]
            return IngestionResult(
                id=record["id"],
                status="success",
                embedding_generated=True,
                stored_at=datetime.fromisoformat(
                    record["created_at"].replace("Z", "+00:00")
                ),
            )
        except Exception as e:
            logger.error(f"Lyrics ingestion failed: {e}")
            return IngestionResult(
                id="",
                status="failed",
                embedding_generated=True,
                stored_at=datetime.now(),
            )

    async def update_lyrics_status(
        self, lyrics_id: str, status: str, embedding: Optional[List[float]] = None
    ) -> bool:
        """Update lyrics status after processing."""
        try:
            update_data = {"status": status}
            if embedding is not None:
                update_data["embedding"] = embedding

            self.client.table("lyrics").update(update_data).eq(
                "id", lyrics_id
            ).execute()

            return True
        except Exception as e:
            logger.error(f"Status update failed: {e}")
            return False

    async def complete_lyrics(
        self,
        lyrics_id: str,
        embedding: Optional[List[float]] = None,
        vocabulary: Optional[List[Dict]] = None,
    ) -> bool:
        """Mark lyrics as complete with final embedding."""
        return await self.update_lyrics_status(lyrics_id, "complete", embedding)

    async def save_agent_session(self, session_data: Dict[str, Any]) -> str:
        """
        Save agent session to Supabase for persistent memory.

        Args:
            session_data: Session information including summary, decisions

        Returns:
            Session ID
        """
        try:
            result = self.client.table("agent_sessions").insert(session_data).execute()
            return result.data[0]["id"]
        except Exception as e:
            logger.error(f"Session save failed: {e}")
            raise

    async def get_health(self) -> Dict[str, Any]:
        """Check service health."""
        return {
            "status": "healthy" if self._connected else "disconnected",
            "supabase": self._connected,
            "config": {
                "embedding_model": self.config.embedding_model,
                "match_threshold": self.config.match_threshold,
                "query_expansion": self.config.enable_query_expansion,
            },
        }
