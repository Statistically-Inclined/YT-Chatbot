
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.config.constants import COMMENTS_CHUNK_OVERLAP, COMMENTS_CHUNK_SIZE

def split_comments_to_summary(comment_list: List[str]):
    """Split the combined comment text into manageable chunks."""

    try:
        all_comments = " ".join(comment_list)
        splitter = RecursiveCharacterTextSplitter(chunk_size=COMMENTS_CHUNK_SIZE,
                                                  chunk_overlap=COMMENTS_CHUNK_OVERLAP)
        
        chunks = splitter.create_documents([all_comments])
        logger.info(f"Comments split into {len(chunks)} chunks.")

        return chunks
    
    except Exception as e:
        logger.exception("Failed to split comments into chunks.")
        raise ProcessingError("Chunking comments failed.") from e
