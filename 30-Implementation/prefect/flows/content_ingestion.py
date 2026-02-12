# Content Ingestion Flow

"""
Content Ingestion: YouTube → Database pipeline.

This flow processes YouTube videos into the KLM content database.

Usage:
    python flows/content_ingestion.py
"""

from prefect import flow, task
from typing import List, Dict
import logging
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from tasks.youtube_tasks import download_youtube_audio, extract_video_metadata
from tasks.whisper_tasks import transcribe_audio
from tasks.gemini_tasks import analyze_transcription, generate_visual_prompt

logger = logging.getLogger(__name__)


@task(retries=2, retry_delay_seconds=60)
def save_to_database(content: Dict) -> Dict:
    """
    Save processed content to Supabase database.

    Args:
        content: Processed content item

    Returns:
        Database save result
    """
    # TODO: Implement Supabase integration
    logger.info(f"Saving to database: {content.get('title', 'Unknown')}")

    result = {"saved": True, "id": content.get("video_id"), "status": "PENDING_REVIEW"}

    return result


@flow(name="Content Ingestion")
def content_ingestion_flow(video_urls: List[str]) -> List[Dict]:
    """
    Main content ingestion flow.

    YouTube URL → Download → Transcribe → Analyze → Database

    Args:
        video_urls: List of YouTube URLs

    Returns:
        List of processed content results
    """
    logger.info("=" * 50)
    logger.info("CONTENT INGESTION STARTED")
    logger.info(f"Processing {len(video_urls)} videos")
    logger.info("=" * 50)

    results = []

    for url in video_urls:
        try:
            # Extract video ID
            video_id = url.split("v=")[1] if "v=" in url else url.split("/")[-1]
            logger.info(f"Processing: {video_id}")

            # Download audio
            audio_path = download_youtube_audio(video_id)

            # Extract metadata
            metadata = extract_video_metadata(video_id)

            # Transcribe
            transcription = transcribe_audio(audio_path)

            # Analyze with Gemini
            analysis = analyze_transcription(transcription)

            # Generate visual prompt
            visual_prompt = generate_visual_prompt(analysis)

            # Compile content
            content = {
                "video_id": video_id,
                "url": url,
                "metadata": metadata,
                "transcription": transcription,
                "analysis": analysis,
                "visual_prompt": visual_prompt,
                "quality_score": 0.0,  # Will be set by quality gate
            }

            # Save to database
            saved = save_to_database(content)
            content["db_status"] = saved

            results.append(content)

            logger.info(f"Completed: {metadata.get('title', video_id)}")

        except Exception as e:
            logger.error(f"Failed to process {url}: {e}")
            results.append({"url": url, "status": "ERROR", "error": str(e)})

    logger.info("=" * 50)
    logger.info(f"CONTENT INGESTION COMPLETE: {len(results)} processed")
    logger.info("=" * 50)

    return results


if __name__ == "__main__":
    # Example usage
    test_urls = [
        "https://www.youtube.com/watch?v=EXAMPLE1",
        "https://www.youtube.com/watch?v=EXAMPLE2",
    ]

    # Run flow
    results = content_ingestion_flow(test_urls)
    print(f"Processed {len(results)} videos")
