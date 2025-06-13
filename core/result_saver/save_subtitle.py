
import os
import json
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.config.directory_config import SUBTITLE_DIR

os.makedirs(SUBTITLE_DIR, exist_ok=True)

def save_subtitle_to_txt(cleaned_text, txt_filename="transcript_subtitle.txt"):
    txt_path = os.path.join(SUBTITLE_DIR, txt_filename)
    try:
        with open(txt_path, "w", encoding="utf-8") as txt_out:
            txt_out.write(cleaned_text)
        
        logger.info(f"Transcript Subtitle saved to TXT: {txt_path}")
    
    except Exception as e:
        logger.exception(f"Failed to save transcript to json: {txt_path}")
        raise ProcessingError(f"Error saving transcript to json: {str(e)}")


def save_subtitle_to_json(transcript_data, json_filename="transcript_subtitle.json"):
    json_path = os.path.join(SUBTITLE_DIR, json_filename)
    try:
        with open(json_path, "w", encoding="utf-8") as json_out:
            json.dump(transcript_data, json_out, indent=2, ensure_ascii=False)
        
        logger.info(f"Transcript Subtitle saved to JSON: {json_path}")

    except Exception as e:
        logger.exception(f"Failed to save transcript to json: {json_path}")
        raise ProcessingError(f"Error saving transcript to json: {str(e)}")
