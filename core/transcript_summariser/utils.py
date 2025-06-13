
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.config.constants import TRANSCRIPT_CHUNK_SIZE, TRANSCRIPT_CHUNK_OVERLAP_SUMMARY


def split_transcript_for_summary(transcript: str):
    """Splits transcript into large chunks suitable for summarization."""

    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=TRANSCRIPT_CHUNK_SIZE, chunk_overlap=TRANSCRIPT_CHUNK_OVERLAP_SUMMARY)
        chunks = splitter.create_documents([transcript])

        logger.info(f"Transcript split into {len(chunks)} chunks for summarization.")

        return chunks
    
    except Exception as e:
        logger.exception("Failed to split transcript for summarization.")
        raise ProcessingError("Transcript splitting for summarization failed.") from e
