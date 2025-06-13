
import os
from datetime import datetime
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.config.directory_config import TRANSCRIPT_SUMMARY_DIR
from core.config.directory_config import COMMENT_SUMMARY_DIR


os.makedirs(TRANSCRIPT_SUMMARY_DIR, exist_ok=True)
os.makedirs(COMMENT_SUMMARY_DIR, exist_ok=True)


def save_transcript_summary_to_txt(final_summary: str, base_filename: str = "transcript_summary") -> str:
    """ Save the summary text to a timestamped .txt file in the transcript summary directory. """

    try:
        # Add filename
        filename = f"{base_filename}.txt"
        file_path = os.path.join(TRANSCRIPT_SUMMARY_DIR, filename)

        # Write summary to file
        with open(file_path, "w", encoding="utf-8") as txt_out:
            txt_out.write(final_summary)

        logger.info(f"Summary successfully saved to: {file_path}")
        
        return file_path

    except Exception as e:
        logger.exception(f"Failed to save summary to TXT: {e}")
        raise ProcessingError(f"Error saving summary to TXT: {str(e)}") from e


def save_comment_summary_to_txt(final_summary: str, base_filename: str = "comment_summary") -> str:
    """ Save the summary text to a timestamped .txt file in the transcript summary directory. """

    try:
        # Add filename
        filename = f"{base_filename}.txt"
        file_path = os.path.join(COMMENT_SUMMARY_DIR, filename)

        formatted_text = final_summary.replace('.', '.*\n')

        # Write summary to file
        with open(file_path, "w", encoding="utf-8") as txt_out:
            txt_out.write(formatted_text)

        logger.info(f"Summary successfully saved to: {file_path}")
        
        return file_path

    except Exception as e:
        logger.exception(f"Failed to save summary to TXT: {e}")
        raise ProcessingError(f"Error saving summary to TXT: {str(e)}") from e
