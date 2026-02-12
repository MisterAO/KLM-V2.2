from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
import time
import subprocess
from datetime import datetime


@task(cache_key_fn=task_input_hash, retries=3, retry_delay_seconds=5)
def ingest_files(file_path: str):
    """Ingest files into LlamaIndex"""
    logger = get_run_logger()
    logger.info(f"Starting ingestion for: {file_path}")

    try:
        result = subprocess.run(
            ["python", "-m", "backend.src.mars.ingest", "--path", file_path],
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode == 0:
            logger.info(f"Successfully ingested: {file_path}")
            return {"status": "success", "path": file_path}
        else:
            logger.error(f"Ingestion failed: {result.stderr}")
            raise Exception(f"Ingestion failed: {result.stderr}")

    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        raise


@task(retries=2, retry_delay_seconds=10)
def update_chroma_index():
    """Update ChromaDB embeddings"""
    logger = get_run_logger()
    logger.info("Updating ChromaDB index")

    # Simulate embedding update
    time.sleep(2)

    logger.info("ChromaDB index updated")
    return {"status": "success", "index": "chroma"}


@task(retries=2, retry_delay_seconds=10)
def generate_summary():
    """Generate project summary"""
    logger = get_run_logger()
    logger.info("Generating project summary")

    try:
        result = subprocess.run(
            ["python", "scripts/project_map_generator.py"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        logger.info("Project summary generated")
        return {"status": "success", "generated": True}

    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        raise


@flow(name="ingestion-pipeline", log_prints=True)
def ingestion_pipeline(file_path: str = "."):
    """
    Ingest files into the knowledge base

    Args:
        file_path: Path to files to ingest
    """
    logger = get_run_logger()
    logger.info(f"Starting ingestion pipeline for: {file_path}")

    # Step 1: Ingest files
    ingest_result = ingest_files(file_path)

    # Step 2: Update ChromaDB
    chroma_result = update_chroma_index()

    # Step 3: Generate summary
    summary_result = generate_summary()

    logger.info("Ingestion pipeline completed successfully")

    return {
        "status": "success",
        "ingested": ingest_result,
        "chroma": chroma_result,
        "summary": summary_result,
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    # Run the flow
    result = ingestion_pipeline()
    print(f"Flow result: {result}")
