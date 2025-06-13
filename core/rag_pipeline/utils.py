
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.config.constants import RAG_CHUNK_SIZE, RAG_CHUNK_OVERLAP


def split_transcript(transcript: str):
    """Split a transcript into chunks for processing."""

    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=RAG_CHUNK_SIZE, chunk_overlap=RAG_CHUNK_OVERLAP)
        chunks = splitter.create_documents([transcript])
        logger.info(f"Transcript split into {len(chunks)} chunks.")

        return chunks
    
    except Exception as e:
        logger.exception("Failed to split transcript.")
        raise ProcessingError("Transcript splitting failed.") from e


def build_vector_store(chunks, embeddings):
    """Create FAISS vector store from chunks using provided embeddings."""

    try:
        vector_store = FAISS.from_documents(chunks, embeddings)
        logger.info("Vector store created successfully.")

        return vector_store
    
    except Exception as e:
        logger.exception("Failed to create vector store.")
        raise ProcessingError("Vector store creation failed.") from e


def get_retriever(vector_store):
    """Initialize a retriever from vector store."""

    try:
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        logger.info("Retriever initialized.")

        return retriever
    
    except Exception as e:
        logger.exception("Failed to create retriever.")
        raise ProcessingError("Retriever creation failed.") from e
    
    
def format_docs(retrieved_docs: List):
    """Format retrieved documents into a single string for LLM context."""

    try:
        return "\n\n".join(doc.page_content for doc in retrieved_docs)
    
    except Exception as e:
        logger.exception("Failed to format retrieved documents.")
        raise ProcessingError("Document formatting failed.") from e



