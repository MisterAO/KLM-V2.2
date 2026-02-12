# YouTube Tasks

"""
YouTube-related Prefect tasks.
"""

from prefect import task
from typing import Dict, List, Optional
import logging
import yt_dlp
import os

logger = logging.getLogger(__name__)


@task(retries=3, retry_delay_seconds=30)
def download_youtube_audio(
    video_id: str, output_dir: str = "assets/audio_in", format: str = "bestaudio"
) -> str:
    """
    Download audio from YouTube video.

    Args:
        video_id: YouTube video ID
        output_dir: Output directory
        format: Audio format

    Returns:
        Path to downloaded audio file
    """
    os.makedirs(output_dir, exist_ok=True)

    output_template = f"{output_dir}/%(id)s.%(ext)s"

    ydl_opts = {
        "format": format,
        "outtmpl": output_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "postprocessor_args": [
            "-metadata",
            "title=",
            "-metadata",
            "artist=",
        ],
        "quiet": False,
        "no_warnings": False,
    }

    url = f"https://www.youtube.com/watch?v={video_id}"

    logger.info(f"Downloading: {url}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        audio_path = f"{output_dir}/{video_id}.mp3"
        logger.info(f"Downloaded: {audio_path}")
        return audio_path

    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise


@task(retries=2)
def extract_video_metadata(video_id: str) -> Dict:
    """
    Extract metadata from YouTube video.

    Args:
        video_id: YouTube video ID

    Returns:
        Video metadata dictionary
    """
    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        metadata = {
            "video_id": video_id,
            "title": info.get("title"),
            "artist": info.get("uploader"),
            "duration": info.get("duration"),
            "view_count": info.get("view_count"),
            "upload_date": info.get("upload_date"),
            "thumbnail": info.get("thumbnail"),
            "url": url,
        }

        logger.info(f"Metadata extracted: {metadata['title']}")
        return metadata

    except Exception as e:
        logger.error(f"Metadata extraction failed: {e}")
        raise


@task
def validate_video_id(video_id: str) -> bool:
    """
    Validate YouTube video ID format.

    Args:
        video_id: Video ID to validate

    Returns:
        True if valid
    """
    import re

    pattern = r"^[a-zA-Z0-9_-]{11}$"
    is_valid = bool(re.match(pattern, video_id))

    if not is_valid:
        logger.warning(f"Invalid video ID: {video_id}")

    return is_valid
