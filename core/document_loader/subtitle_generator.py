
import os
import time
import yt_dlp
import webvtt
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError, ResourceNotFoundError
from core.config.directory_config import SUBTITLE_DIR, DEFAULT_VTT_FILE


output_template = os.path.join(SUBTITLE_DIR, "transcript_temp")


def download_subtitles(video_url: str, output_template: str = output_template) -> str:
    """
    Download automatic English subtitles from a YouTube video using yt_dlp.
    """

    try:
        # Ensure the subtitle directory exists
        os.makedirs(SUBTITLE_DIR, exist_ok=True)

        options = {
            'skip_download': True,
            'writesubtitles': False,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'vtt',
            'outtmpl': output_template,
            'noplaylist': True
        }

        for attempt in range(5):

            logger.info(f"Requesting Subtitle... Retrying Attempt: {attempt+1}")

            try:
                with yt_dlp.YoutubeDL(options) as ydl:
                    logger.info(f"[Attempt {attempt+1}/5] Downloading subtitles for URL: {video_url}")
                    ydl.download([video_url])
                    logger.info(f"Subtitle downloaded to {output_template}")

                    return output_template
                
            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed: {e}")
                if attempt < 4:
                    time.sleep(2)  # wait before retrying
                else:
                    raise

    except Exception as e:
        logger.error(f"Failed to download subtitles after retries: {e}")
        raise ProcessingError("Error occurred while downloading subtitles.")


def parse_and_clean_vtt(vtt_filename: str = DEFAULT_VTT_FILE) -> tuple[str, list[dict]]:
    """
    Parse a .vtt subtitle file and return cleaned transcript text and structured caption list.
    """

    transcript_list = []
    transcript_text = ""

    try:
        # Parse captions from VTT file
        for caption in webvtt.read(vtt_filename):
            line = caption.text.strip()
            transcript_list.append({
                "start": caption.start,
                "end": caption.end,
                "text": line
            })
            transcript_text += line + "\n"

        # Remove duplicate consecutive lines
        lines = transcript_text.strip().splitlines()
        cleaned_lines = []
        previous_line = None
        for line in lines:
            if line != previous_line:
                cleaned_lines.append(line)
            previous_line = line

        cleaned_text = "\n".join(cleaned_lines)
        logger.info(f"Parsed and cleaned subtitles from {vtt_filename}")

        return cleaned_text, transcript_list

    except FileNotFoundError:
        logger.error(f"Subtitle file not found: {vtt_filename}")
        raise ResourceNotFoundError(f"Subtitle file not found: {vtt_filename}")
    
    except Exception as e:
        logger.error(f"Failed to parse VTT file: {e}")
        raise ProcessingError("Error occurred while parsing subtitles.")


def generate_subtitles_from_youtube_url(video_url: str) -> tuple[str, list[dict]]:
    """ Wrapper function that downloads automatic subtitles from a YouTube video
        and parses + cleans the resulting .vtt file."""
    
    try:
        output_template = download_subtitles(video_url)
        vtt_filename = f"{output_template}.en.vtt"
        cleaned_text, transcript_list = parse_and_clean_vtt(vtt_filename)

        return cleaned_text, transcript_list

    except (ProcessingError, ResourceNotFoundError) as e:
        logger.error(f"Subtitle generation failed: {e}")
        raise ProcessingError("Error occurred while parsing subtitles.")
