# Whisper Transcription Tasks

"""
Audio transcription using OpenAI Whisper.
"""

from prefect import task
from typing import Dict, Optional
import logging
import whisper
import torch

logger = logging.getLogger(__name__)


@task(retries=2, retry_delay_seconds=60)
def transcribe_audio(
    audio_path: str,
    model_size: str = "base",
    language: str = "km",  # Khmer
) -> Dict:
    """
    Transcribe audio using Whisper.

    Args:
        audio_path: Path to audio file
        model_size: Whisper model size (tiny, base, small, medium, large)
        language: Language code (km = Khmer)

    Returns:
        Transcription result with segments
    """
    logger.info(f"Transcribing: {audio_path}")

    # Load model (CPU mode sufficient for POC)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Using device: {device}")

    model = whisper.load_model(model_size, device=device)

    # Transcribe
    result = model.transcribe(audio_path, language=language, verbose=False)

    # Format result
    transcription = {
        "text": result["text"],
        "segments": [
            {
                "id": segment["id"],
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"],
            }
            for segment in result.get("segments", [])
        ],
        "language": result.get("language", language),
        "audio_path": audio_path,
        "model": f"whisper-{model_size}",
    }

    logger.info(f"Transcription complete: {len(transcription['segments'])} segments")

    return transcription


@task
def extract_lyrics_segments(transcription: Dict) -> list:
    """
    Extract clean lyrics segments from transcription.

    Args:
        transcription: Whisper transcription result

    Returns:
        List of {start, end, text} segments
    """
    segments = transcription.get("segments", [])

    lyrics = []
    for segment in segments:
        text = segment.get("text", "").strip()
        if text:
            lyrics.append(
                {
                    "start": segment.get("start", 0),
                    "end": segment.get("end", 0),
                    "text": text,
                }
            )

    logger.info(f"Extracted {len(lyrics)} lyric segments")
    return lyrics


@task
def detect_language(transcription: Dict) -> str:
    """
    Detect language from transcription.

    Args:
        transcription: Whisper result

    Returns:
        Detected language code
    """
    return transcription.get("language", "unknown")
