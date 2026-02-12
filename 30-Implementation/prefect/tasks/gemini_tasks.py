# Gemini AI Tasks

"""
AI analysis using Google Gemini.
"""

from prefect import task
from typing import Dict, List, Optional
from google import genai
import logging
import os

logger = logging.getLogger(__name__)


@task(retries=2, retry_delay_seconds=30)
def analyze_transcription(
    transcription: Dict, prompt_type: str = "full_analysis"
) -> Dict:
    """
    Analyze transcription using Gemini.

    Args:
        transcription: Whisper transcription
        prompt_type: Type of analysis (full_analysis, cultural, lyrics)

    Returns:
        AI-generated analysis
    """
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    text = transcription.get("text", "")
    segments = transcription.get("segments", [])

    # Build prompt based on type
    if prompt_type == "full_analysis":
        prompt = f"""
        Analyze these Khmer song lyrics:
        
        {text}
        
        Provide:
        1. English translation
        2. Romanization
        3. Cultural context
        4. Key vocabulary (with definitions)
        5. Historical significance (1960-1975 era)
        """
    elif prompt_type == "cultural":
        prompt = f"""
        Provide cultural and historical context for this 1960s-1970s Khmer song:
        
        {text}
        
        Focus on:
        - Cultural references
        - Historical context
        - Musical significance
        """
    elif prompt_type == "lyrics":
        prompt = f"""
        Format these Khmer lyrics with romanization and translation:
        
        {text}
        
        Format as JSON:
        {{
            "romanization": "...",
            "translation": "...",
            "vocabulary": [
                {{"word": "...", "definition": "..."}}
            ]
        }}
        """
    else:
        prompt = f"Analyze: {text}"

    logger.info(f"Calling Gemini ({prompt_type})...")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )

        result = {
            "analysis": response.text,
            "prompt_type": prompt_type,
            "model": "gemini-2.5-flash",
            "input_length": len(text),
        }

        logger.info(f"Analysis complete: {len(response.text)} chars")
        return result

    except Exception as e:
        logger.error(f"Gemini analysis failed: {e}")
        raise


@task
def generate_visual_prompt(analysis: Dict, style: str = "aokhmer") -> str:
    """
    Generate visual prompt for ComfyUI.

    Args:
        analysis: Gemini analysis result
        style: Visual style (aokhmer, klm)

    Returns:
        Prompt string for image generation
    """
    # Brand-compliant prompts
    if style == "aokhmer":
        prompt = f"""
        {analysis.get("analysis", "")[:500]}
        
        Style: 1960s Cambodian Psychedelic Rock poster art
        Lighting: Wong Kar-wai neon noir, golden hour
        Colors: Mekong Gold (#EBCB00), Deep Teal (#374C57)
        Quality: 8k, film grain
        """
    else:
        prompt = f"""
        {analysis.get("analysis", "")[:500]}
        
        Style: Clean educational interface
        Colors: Deep Teal (#374C57), Mekong Gold (#EBCB00)
        """

    logger.info(f"Generated {style} visual prompt")
    return prompt.strip()


@task
def validate_cultural_accuracy(analysis: Dict) -> Dict:
    """
    Validate cultural accuracy of analysis.

    Args:
        analysis: Gemini analysis

    Returns:
        Validation result with score
    """
    # TODO: Implement RAG-based validation with ChromaDB
    # For now, return placeholder

    validation = {
        "cultural_accuracy_score": 0.85,
        "flags": [],
        "verified": True,
        "notes": "Placeholder - implement RAG validation",
    }

    logger.info(f"Cultural validation: {validation['verified']}")
    return validation
