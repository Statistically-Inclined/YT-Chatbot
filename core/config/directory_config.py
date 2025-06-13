
import os

BASE_DIR = "youtube_data"
OUTPUT_DIR = "output"

COMMENTS_DIR = os.path.join(BASE_DIR, "comments")
METADATA_DIR = os.path.join(BASE_DIR, "metadata")
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcript")
SUBTITLE_DIR = os.path.join(BASE_DIR, "subtitle")

TRANSCRIPT_SUMMARY_DIR = os.path.join(OUTPUT_DIR, "transcript_summary")
COMMENT_SUMMARY_DIR = os.path.join(OUTPUT_DIR, "comments_summary")
METADATA_FORMATTED_DIR = os.path.join(OUTPUT_DIR, "metadata_formatted")

# 💡 Optional: default subtitle file path
DEFAULT_VTT_FILE = os.path.join(SUBTITLE_DIR, "transcript_temp.en.vtt")