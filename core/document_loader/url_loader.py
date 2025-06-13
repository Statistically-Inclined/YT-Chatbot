
import re
import requests
from urllib.parse import urlparse, parse_qs
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError, ResourceNotFoundError


def validate_youtube_url(url: str) -> str:
    """Checks if the URL is a valid and publicly accessible YouTube video."""

    try:
        logger.debug(f"Validating YouTube video URL: {url}")
        parsed = urlparse(url)

        if parsed.netloc not in ("www.youtube.com", "youtube.com", "youtu.be"):
            logger.error(f"Rejected non-YouTube URL: {url}")
            raise ResourceNotFoundError("Only YouTube video URLs are accepted.")

        if not parsed.scheme.startswith("http"):
            logger.error(f"Invalid URL scheme in: {url}")
            raise ResourceNotFoundError("Invalid URL format.")

        response = requests.get(url, timeout=5)
        if response.status_code >= 400:
            logger.warning(f"Received error status {response.status_code} for URL: {url}")
            raise ResourceNotFoundError("YouTube video URL is not reachable.")

        content = response.text.lower()
        unavailable_indicators = [
            "video unavailable",
            "this video is private",
            "this video has been removed",
            "this video is no longer available",
            "age-restricted video",
        ]

        if any(indicator in content for indicator in unavailable_indicators):
            logger.warning(f"Video appears unavailable: {url}")
            raise ResourceNotFoundError("YouTube video is unavailable or restricted.")

        logger.info(f"Video is valid and available: {url}")

        return url

    except requests.RequestException as e:
        logger.exception("Network error while validating YouTube video URL.")
        raise ProcessingError("Network error during YouTube video validation.") from e


def extract_video_id_from_url(url: str) -> str:
    """Extracts the video ID from a valid YouTube URL."""

    try:
        logger.debug(f"Extracting video ID from URL: {url}")
        parsed = urlparse(url)
        video_id = None

        if parsed.hostname in ("www.youtube.com", "youtube.com"):
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif parsed.hostname == "youtu.be":
            video_id = parsed.path.lstrip("/")
        else:
            match = re.search(r"(?:v=|\/|embed\/)([0-9A-Za-z_-]{11})", url)
            video_id = match.group(1) if match else None

        if not video_id:
            logger.error(f"Video ID extraction failed: {url}")
            raise ResourceNotFoundError("Could not extract video ID from URL.")

        logger.info(f"Extracted video ID: {video_id}")

        return video_id

    except Exception as e:
        logger.exception("Error extracting video ID.")
        raise ProcessingError("Failed to extract YouTube video ID.") from e


def get_youtube_video_id_and_url(url: str) -> tuple[str, str]:
    """Wrapper to validate YouTube video and extract its video ID."""

    logger.debug(f"Starting process to get video ID and validate URL: {url}")

    try:
        validated_url = validate_youtube_url(url)
        video_id = extract_video_id_from_url(validated_url)
        logger.info(f"Successfully retrieved video ID '{video_id}' from URL.")
        
        return video_id, validated_url

    except (ProcessingError, ResourceNotFoundError) as e:
        logger.error(f"Failed to process YouTube URL: {url} | Reason: {e}")
        raise