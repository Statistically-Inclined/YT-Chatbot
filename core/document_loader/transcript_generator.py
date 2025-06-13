
import time
from typing import List, Tuple, Optional
from core.config.logger_config import logger
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from core.config.exceptions import ProcessingError, ResourceNotFoundError


def retry_get_transcript(video_id: str, lang_code: str, retries: int = 10) -> Optional[List[dict]]:
    """Retry fetching transcript for a video in a specific language"""

    for attempt in range(retries):

        logger.info(f"Requesting Transcript... Retrying Attempt: {attempt+1}")

        try:
            return YouTubeTranscriptApi.get_transcript(video_id, languages=[lang_code])
        
        except Exception as e:
            logger.warning(f"Retrying transcript fetch: {lang_code} ({attempt + 1}/{retries}) due to {e}")
            time.sleep(2)

    raise ProcessingError(f"Failed to retrieve transcript for language '{lang_code}' after {retries} retries.")


def get_transcript_with_priority(video_id: str, priority_lang: str = "en", retries: int = 10) -> Tuple[Optional[List[dict]], Optional[str]]:
    """Fetch transcript with preferred language, fallback to available"""
    
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        all_langs = [t.language_code for t in transcripts]
        logger.info(f"Available transcript languages: {all_langs}")

        lang_to_use = priority_lang if priority_lang in all_langs else all_langs[0] if all_langs else None
        if not lang_to_use:
            logger.error("No transcripts available")
            raise ResourceNotFoundError("Transcript not available in any language.")

        transcript_chunks = retry_get_transcript(video_id, lang_to_use, retries)

        if transcript_chunks:
            transcript = " ".join(chunk["text"] for chunk in transcript_chunks)
            logger.info(f"Transcript found using language: {lang_to_use}")

            return transcript_chunks, transcript

    except TranscriptsDisabled:
        logger.error("Transcripts are disabled for this video.")
        raise ProcessingError("Transcripts are disabled for this video.")
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise ProcessingError(f"Failed to get transcript: {e}")

    return None, None
