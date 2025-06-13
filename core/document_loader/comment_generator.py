
import time
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError


def get_video_comments(youtube_client, video_id: str, max_comments: int = 50) -> list[dict]:
    """
    Fetch top-level comments from a YouTube video using the YouTube Data API, with retries.
    """

    comments = []
    next_page_token = None
    max_retries = 10
    delay = 1  # seconds

    try:
        while len(comments) < max_comments:
            for attempt in range(1, max_retries + 1):

                logger.info(f"Requesting Comments... Retrying Attempt: {attempt}")
                
                try:
                    request = youtube_client.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        maxResults=min(100, max_comments - len(comments)),
                        pageToken=next_page_token,
                        textFormat="plainText"
                    )

                    logger.debug(f"Requesting comments page with pageToken={next_page_token} (Attempt {attempt})")
                    response = request.execute()
                    break  # Break retry loop if successful

                except Exception as e:
                    logger.warning(f"Attempt {attempt} failed while fetching comments: {e}")
                    if attempt < max_retries:
                        time.sleep(delay)
                    else:
                        logger.exception(f"All {max_retries} attempts failed while fetching comments.")
                        raise ProcessingError("Comments fetch failed") from e

            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "author": snippet.get("authorDisplayName"),
                    "text": snippet.get("textDisplay"),
                    "like_count": snippet.get("likeCount", 0),
                    "published_at": snippet.get("publishedAt"),
                    "updated_at": snippet.get("updatedAt")
                })

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

            # Slight delay to respect API rate limits
            time.sleep(0.1)

        logger.info(f"Fetched {len(comments)} comments for video ID: {video_id}")
        return comments

    except Exception as e:
        logger.exception(f"Error fetching comments for video ID {video_id}")
        raise ProcessingError("Comments fetch failed") from e

