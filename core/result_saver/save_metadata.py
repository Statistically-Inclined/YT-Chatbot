
import os
import json
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.config.directory_config import METADATA_DIR


os.makedirs(METADATA_DIR, exist_ok=True)

def save_metadata_to_json(metadata, filename="metadata.json"):
    """
    Save metadata dictionary to a JSON file.
    """

    filepath = os.path.join(METADATA_DIR, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)
        logger.info(f"Video metadata saved to JSON: {filepath}")

    except Exception as e:
        logger.exception(f"Failed to save metadata to JSON: {filepath}")
        raise ProcessingError(f"Error saving video metadata: {str(e)}")


def save_metadata_to_text(metadata: dict, filename="metadata.txt"):
    """
    Save metadata dictionary directly to a human-readable text file.
    """

    filepath = os.path.join(METADATA_DIR, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")  # Write each key-value pair on a new line
        logger.info(f"Video metadata saved to text: {filepath}")

    except Exception as e:
        logger.exception(f"Failed to save metadata to text: {filepath}")
        raise ProcessingError(f"Error saving metadata to text: {str(e)}")
