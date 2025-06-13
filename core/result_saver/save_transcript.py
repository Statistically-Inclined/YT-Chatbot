
import os
import json
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.config.directory_config import TRANSCRIPT_DIR

os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

def save_transcript_to_txt(transcript_chunks, filename="transcript.txt"):
    filepath = os.path.join(TRANSCRIPT_DIR, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for i, c in enumerate(transcript_chunks, start=1):
                f.write(f"{i}. {c['text']}\n")

        logger.info(f"Transcript saved to TXT: {filepath}")

    except Exception as e:
        logger.exception(f"Failed to save transcript to txt: {filepath}")
        raise ProcessingError(f"Error saving transcript to txt: {str(e)}")


def save_transcript_to_json(transcript_chunk, filename="transcript.json"):
    filepath = os.path.join(TRANSCRIPT_DIR, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(transcript_chunk, f, indent=4)

        logger.info(f"Transcript saved to JSON: {filepath}")

    except Exception as e:
        logger.exception(f"Failed to save transcript to json: {filepath}")
        raise ProcessingError(f"Error saving transcript to json: {str(e)}")
