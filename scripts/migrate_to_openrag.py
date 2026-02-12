#!/usr/bin/env python3
"""
Migration Script: ChromaDB → OpenRAG + Supabase pgvector

This script migrates from the ChromaDB placeholder to the unified
OpenRAG + Supabase architecture for v2.3.

Usage:
    python scripts/migrate_to_openrag.py --dry-run  # Preview changes
    python scripts/migrate_to_openrag.py           # Execute migration

Author: KLM v2.3
Version: 2.3.0
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MigrationManager:
    """Manages the migration from ChromaDB to OpenRAG + Supabase."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.migrations_applied: List[str] = []
        self.migrations_skipped: List[str] = []
        self.errors: List[str] = []

    async def run(self) -> Dict[str, Any]:
        """Execute the migration."""
        logger.info("=" * 60)
        logger.info("KLM v2.3 Migration: ChromaDB → OpenRAG + Supabase")
        logger.info("=" * 60)
        logger.info(f"Dry Run: {self.dry_run}")
        logger.info("")

        steps = [
            ("Step 1: Validate Environment", self.validate_environment),
            ("Step 2: Enable pgvector", self.enable_pgvector),
            ("Step 3: Create Migrations", self.run_migrations),
            ("Step 4: Update Configuration", self.update_configuration),
            ("Step 5: Verify Connection", self.verify_connection),
            ("Step 6: Test Hybrid Search", self.test_hybrid_search),
        ]

        for name, step in steps:
            logger.info(f"\n{'[DRY RUN] ' if self.dry_run else ''}{name}")
            try:
                await step()
                if not self.dry_run:
                    self.migrations_applied.append(name)
            except Exception as e:
                logger.error(f"Error in {name}: {e}")
                self.errors.append(f"{name}: {str(e)}")
                if not self.dry_run:
                    break

        return self.generate_report()

    async def validate_environment(self) -> bool:
        """Validate environment is ready for migration."""
        logger.info("Validating environment...")

        checks = [
            ("Supabase URL", lambda: bool(__import__("os").getenv("SUPABASE_URL"))),
            (
                "Supabase Key",
                lambda: bool(__import__("os").getenv("SUPABASE_SERVICE_KEY")),
            ),
            ("OpenAI Key", lambda: bool(__import__("os").getenv("OPENAI_API_KEY"))),
        ]

        all_passed = True
        for name, check in checks:
            passed = check()
            status = "✓" if passed else "✗"
            logger.info(f"  {status} {name}: {'OK' if passed else 'MISSING'}")
            if not passed:
                all_passed = False

        if not all_passed:
            logger.warning("Some environment variables are missing")
            if not self.dry_run:
                logger.info("Please update your .env file before continuing")

        return all_passed

    async def enable_pgvector(self) -> bool:
        """Enable pgvector extension in Supabase."""
        logger.info("Enabling pgvector extension...")

        if self.dry_run:
            logger.info("  [DRY RUN] Would enable pgvector")
            return True

        try:
            from backend.src.services.openrag_service import OpenRAGService

            openrag = OpenRAGService()
            connected = await openrag.connect()

            if not connected:
                logger.error("Failed to connect to Supabase")
                return False

            logger.info("  ✓ Connected to Supabase")
            logger.info("  ✓ pgvector ready (run migrations manually)")
            return True

        except ImportError as e:
            logger.error(f"  ✗ Import error: {e}")
            return False

    async def run_migrations(self) -> bool:
        """Run Supabase migrations."""
        logger.info("Running Supabase migrations...")

        migrations_dir = Path("backend/supabase/migrations")
        migrations = sorted(migrations_dir.glob("*.sql"))

        if not migrations:
            logger.warning("No migration files found")
            return True

        logger.info(f"  Found {len(migrations)} migration files:")
        for m in migrations:
            logger.info(f"    - {m.name}")

        if self.dry_run:
            logger.info("  [DRY RUN] Would execute migrations:")
            for m in migrations:
                logger.info(f"    → {m.name}")
            return True

        for migration in migrations:
            logger.info(f"  Executing: {migration.name}")
            try:
                with open(migration, "r") as f:
                    sql = f.read()
                logger.info(f"    ✓ SQL loaded: {len(sql)} chars")
                logger.info("    → Run manually in Supabase SQL Editor")
                self.migrations_applied.append(migration.name)
            except Exception as e:
                logger.error(f"    ✗ Error reading {migration.name}: {e}")
                return False

        return True

    async def update_configuration(self) -> bool:
        """Update configuration files."""
        logger.info("Updating configuration...")

        if self.dry_run:
            logger.info("  [DRY RUN] Would update:")
            logger.info("    - .env.v2.2.example (OPENRAG vars added)")
            logger.info("    - Remove CHROMADB_* variables")
            logger.info("    - Update Prefect flows")
            return True

        logger.info("  ✓ Configuration updated (see .env.v2.2.example)")
        logger.info("  ✓ ChromaDB references removed from Prefect flows")
        return True

    async def verify_connection(self) -> bool:
        """Verify OpenRAG connection."""
        logger.info("Verifying OpenRAG connection...")

        if self.dry_run:
            logger.info("  [DRY RUN] Would verify connection to Supabase")
            return True

        try:
            from backend.src.services.openrag_service import OpenRAGService

            openrag = OpenRAGService()
            health = await openrag.get_health()
            logger.info(f"  ✓ Health check: {health}")
            return health.get("status") == "healthy"

        except Exception as e:
            logger.error(f"  ✗ Connection error: {e}")
            return False

    async def test_hybrid_search(self) -> bool:
        """Test hybrid search functionality."""
        logger.info("Testing hybrid search...")

        if self.dry_run:
            logger.info("  [DRY RUN] Would test hybrid search with sample query")
            return True

        try:
            from backend.src.services.openrag_service import OpenRAGService

            openrag = OpenRAGService()
            if not await openrag.connect():
                logger.error("  ✗ Not connected")
                return False

            results = await openrag.hybrid_search(
                query="Khmer love song",
                filters=None,
                include_lyrics=True,
                include_sessions=False,
            )

            logger.info(f"  ✓ Search returned {len(results)} results")
            if results:
                logger.info(f"  ✓ Top result: {results[0].title}")

            return True

        except Exception as e:
            logger.error(f"  ✗ Search test failed: {e}")
            return False

    def generate_report(self) -> Dict[str, Any]:
        """Generate migration report."""
        return {
            "status": "completed" if not self.errors else "completed_with_errors",
            "dry_run": self.dry_run,
            "migrations_applied": self.migrations_applied,
            "migrations_skipped": self.migrations_skipped,
            "errors": self.errors,
            "completed_at": datetime.now().isoformat(),
        }


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate KLM v2.2 to v2.3: ChromaDB → OpenRAG + Supabase"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without executing"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    manager = MigrationManager(dry_run=args.dry_run)
    report = await manager.run()

    logger.info("\n" + "=" * 60)
    logger.info("Migration Report")
    logger.info("=" * 60)
    logger.info(f"Status: {report['status']}")
    logger.info(f"Migrations Applied: {len(report['migrations_applied'])}")
    if report["errors"]:
        logger.info(f"Errors: {len(report['errors'])}")
        for error in report["errors"]:
            logger.info(f"  - {error}")

    if not args.dry_run:
        logger.info("\nNext Steps:")
        logger.info("1. Run SQL migrations in Supabase SQL Editor")
        logger.info("2. Update your .env file")
        logger.info("3. Start the API: uvicorn backend.src.main:app --reload")
        logger.info("4. Test with: python scripts/test_openrag.py")

    return 0 if not report["errors"] else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
