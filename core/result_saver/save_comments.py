
import os
import csv
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError, ResourceNotFoundError
from core.config.directory_config import COMMENTS_DIR

os.makedirs(COMMENTS_DIR, exist_ok=True)

def save_comments_to_txt(comments, filename="comments.txt"):
    filepath = os.path.join(COMMENTS_DIR, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for i, c in enumerate(comments, start=1):
                f.write(f"{i}. {c['text']}\n")

        logger.info(f"Comments saved to TXT: {filepath}")

    except Exception as e:
        logger.exception(f"Failed to save comments to txt: {filepath}")
        raise ProcessingError(f"Error saving comments to txt: {str(e)}")


def save_comments_to_csv(comments, filename="comments.csv"):
    filepath = os.path.join(COMMENTS_DIR, filename)
    try:
        if not comments:
            raise ResourceNotFoundError("No comments provided to save.")

        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=comments[0].keys())
            writer.writeheader()
            writer.writerows(comments)

        logger.info(f"Comments saved to CSV: {filepath}")

    except Exception as e:
        logger.exception(f"Failed to save comments to csv: {filepath}")
        raise ProcessingError(f"Error saving comments to csv: {str(e)}")
