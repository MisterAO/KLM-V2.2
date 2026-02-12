"""
Ingestion Pipeline - KLM v2.3

Flow for ingesting lyrics and content into Supabase with OpenRAG embeddings.
Replaces old ChromaDB-based flow with unified Supabase + OpenRAG architecture.

Features:
- Zero data drift - metadata and embeddings in same transaction
- Automatic embedding generation via OpenRAG
- Status tracking through processing stages
- Error handling with retries

Author: KLM v2.3
Version: 2.3.0
"""

from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from datetime import datetime
from typing import Dict, Any, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)


@task(cache_key_fn=task_input_hash, retries=3, retry_delay_seconds=5)
async def parse_lyrics_file(file_path: str) -> Dict[str, Any]:
    """
    Parse lyrics file and extract metadata/content.

    Args:
        file_path: Path to lyrics file

    Returns:
        Parsed lyrics data with metadata
    """
    prefect_logger = get_run_logger()
    prefect_logger.info(f"Parsing lyrics file: {file_path}")

    try:
        import os

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        filename = os.path.basename(file_path)
        filename_parts = filename.replace(".txt", "").replace(".csv", "").split("_")

        lyrics_data = {
            "title": filename_parts[0] if filename_parts else "Unknown",
            "artist": filename_parts[1] if len(filename_parts) > 1 else "Unknown",
            "lyrics_khmer": content,
            "metadata": {
                "source_file": file_path,
                "processed_at": datetime.now().isoformat(),
            },
        }

        prefect_logger.info(
            f"Parsed lyrics: {lyrics_data['title']} by {lyrics_data['artist']}"
        )
        return {"status": "success", "data": lyrics_data}

    except Exception as e:
        logger.error(f"Failed to parse {file_path}: {e}")
        raise


@task(retries=3, retry_delay_seconds=10)
async def generate_embedding(text: str) -> list:
    """
    Generate embedding for text using OpenRAG.

    Args:
        text: Text to embed

    Returns:
        Vector embedding
    """
    prefect_logger = get_run_logger()
    prefect_logger.info("Generating embedding via OpenRAG")

    try:
        from backend.src.services.openrag_service import OpenRAGService

        openrag = OpenRAGService()
        if not await openrag.connect():
            raise RuntimeError("Failed to connect to OpenRAG")

        embedding = await openrag.generate_embedding(text)
        prefect_logger.info(f"Generated embedding: {len(embedding)} dimensions")
        return embedding

    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        raise


@task(retries=3, retry_delay_seconds=30)
async def ingest_to_supabase(
    lyrics_data: Dict[str, Any], embedding: list
) -> Dict[str, Any]:
    """
    Ingest lyrics with embedding to Supabase.

    Zero data drift - single transaction for metadata + embedding.

    Args:
        lyrics_data: Parsed lyrics data
        embedding: Generated vector embedding

    Returns:
        Supabase record ID and status
    """
    prefect_logger = get_run_logger()
    prefect_logger.info(f"Ingesting to Supabase: {lyrics_data.get('title')}")

    try:
        from backend.src.services.openrag_service import OpenRAGService

        openrag = OpenRAGService()
        if not await openrag.connect():
            raise RuntimeError("Failed to connect to Supabase")

        result = await openrag.ingest_lyrics(lyrics_data, embedding)

        prefect_logger.info(f"Successfully ingested: {result.id}")
        return {
            "status": "success",
            "id": result.id,
            "embedding_generated": result.embedding_generated,
        }

    except Exception as e:
        logger.error(f"Supabase ingestion failed: {e}")
        raise


@task(retries=2, retry_delay_seconds=60)
async def complete_processing(
    record_id: str, vocabulary: list = None
) -> Dict[str, Any]:
    """
    Mark lyrics as complete after processing.

    Args:
        record_id: Supabase record ID
        vocabulary: Extracted vocabulary list

    Returns:
        Final status
    """
    prefect_logger = get_run_logger()
    prefect_logger.info(f"Completing processing for: {record_id}")

    try:
        from backend.src.services.openrag_service import OpenRAGService

        openrag = OpenRAGService()
        if not await openrag.connect():
            raise RuntimeError("Failed to connect to Supabase")

        success = await openrag.complete_lyrics(
            lyrics_id=record_id, vocabulary=vocabulary
        )

        if success:
            prefect_logger.info(f"Processing complete: {record_id}")
            return {"status": "complete", "id": record_id}
        else:
            raise RuntimeError(f"Failed to complete processing: {record_id}")

    except Exception as e:
        logger.error(f"Processing completion failed: {e}")
        raise


@task(retries=1)
async def handle_error(error: Exception, file_path: str) -> Dict[str, Any]:
    """
    Handle errors during ingestion.

    Args:
        error: The exception that occurred
        file_path: File that caused the error

    Returns:
        Error information for logging
    """
    prefect_logger = get_run_logger()
    prefect_logger.error(f"Error processing {file_path}: {error}")
    return {"status": "failed", "file": file_path, "error": str(error)}


@flow(name="ingestion-pipeline-v23", log_prints=True)
async def ingestion_pipeline(
    file_path: str = "assets/raw_lyrics", process_subdirs: bool = True
) -> Dict[str, Any]:
    """
    Main ingestion pipeline for KLM v2.3.

    Ingest lyrics files into Supabase with OpenRAG embeddings.
    Replaces old ChromaDB-based pipeline.

    Args:
        file_path: Path to directory or file to ingest
        process_subdirs: Whether to process subdirectories

    Returns:
        Pipeline execution result with all processed records
    """
    prefect_logger = get_run_logger()
    prefect_logger.info("=" * 60)
    prefect_logger.info("KLM v2.3 Ingestion Pipeline Starting")
    prefect_logger.info("=" * 60)

    results = {
        "pipeline": "ingestion-pipeline-v23",
        "started_at": datetime.now().isoformat(),
        "status": "success",
        "processed": [],
        "failed": [],
        "summary": {"total": 0, "successful": 0, "failed": 0},
    }

    try:
        import os
        from pathlib import Path

        target_path = Path(file_path)
        files_to_process = []

        if target_path.is_file():
            if target_path.suffix in [".txt", ".csv"]:
                files_to_process.append(str(target_path))
        elif target_path.is_dir():
            pattern = "**/*" if process_subdirs else "*"
            for f in target_path.glob(pattern):
                if f.is_file() and f.suffix in [".txt", ".csv"]:
                    files_to_process.append(str(f))

        prefect_logger.info(f"Found {len(files_to_process)} files to process")

        for idx, file_path in enumerate(files_to_process, 1):
            prefect_logger.info(
                f"Processing {idx}/{len(files_to_process)}: {file_path}"
            )

            try:
                parse_result = await parse_lyrics_file(file_path)
                lyrics_data = parse_result["data"]

                embedding = await generate_embedding(
                    f"{lyrics_data['title']} {lyrics_data.get('lyrics_khmer', '')}"
                )

                ingest_result = await ingest_to_supabase(lyrics_data, embedding)

                complete_result = await complete_processing(
                    record_id=ingest_result["id"], vocabulary=None
                )

                results["processed"].append(
                    {"file": file_path, "id": ingest_result["id"], "status": "success"}
                )
                results["summary"]["successful"] += 1

            except Exception as e:
                error_result = await handle_error(e, file_path)
                results["failed"].append(error_result)
                results["summary"]["failed"] += 1
                prefect_logger.warning(f"Failed to process {file_path}")

            results["summary"]["total"] += 1

    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        results["status"] = "failed"
        results["error"] = str(e)

    results["completed_at"] = datetime.now().isoformat()

    prefect_logger.info("=" * 60)
    prefect_logger.info("Ingestion Pipeline Complete")
    prefect_logger.info(f"Total: {results['summary']['total']}")
    prefect_logger.info(f"Successful: {results['summary']['successful']}")
    prefect_logger.info(f"Failed: {results['summary']['failed']}")
    prefect_logger.info("=" * 60)

    return results


if __name__ == "__main__":
    import sys

    file_path = sys.argv[1] if len(sys.argv) > 1 else "assets/raw_lyrics"
    result = asyncio.run(ingestion_pipeline(file_path))
    print(f"Pipeline result: {result}")
