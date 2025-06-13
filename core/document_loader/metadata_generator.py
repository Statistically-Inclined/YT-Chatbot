
import time
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError, ResourceNotFoundError


def get_video_metadata(youtube_client, video_id: str) -> dict:
    """Fetch metadata for a given YouTube video using the YouTube Data API, with retries."""

    max_retries = 10
    delay = 1  # seconds

    logger.info(f"Fetching metadata for video ID: {video_id}")

    for attempt in range(1, max_retries + 1):
        
        logger.info(f"Requesting Metadata... Retrying Attempt: {attempt}")

        try:
            request = youtube_client.videos().list(part="snippet,statistics", id=video_id)
            response = request.execute()

            video = response["items"][0]

            metadata = {
                "video_id": video_id,
                "title": video["snippet"]["title"],
                "description": video["snippet"]["description"],
                "published_at": video["snippet"]["publishedAt"],
                "channel_title": video["snippet"]["channelTitle"],
                "tags": video["snippet"].get("tags", []),
                "view_count": int(video["statistics"].get("viewCount", 0)),
                "like_count": int(video["statistics"].get("likeCount", 0)),
                "comment_count": int(video["statistics"].get("commentCount", 0))
            }

            logger.info(f"Successfully fetched metadata for video ID: {video_id}")
            return metadata

        except (KeyError, IndexError) as e:
            logger.error(f"No metadata found for video ID: {video_id} - {e}")
            raise ResourceNotFoundError(f"No metadata found for video ID: {video_id}") from e

        except Exception as e:
            logger.warning(f"Attempt {attempt} failed for video ID {video_id}: {e}")
            if attempt < max_retries:
                time.sleep(delay)
            else:
                logger.exception(f"All {max_retries} attempts failed for video ID: {video_id}")
                raise ProcessingError("Failed to fetch video metadata") from e

