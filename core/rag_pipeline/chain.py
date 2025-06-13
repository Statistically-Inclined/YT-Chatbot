
from typing import List
from langchain.schema.runnable import RunnableLambda, RunnableMap
from core.rag_pipeline.utils import format_docs
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError


def build_rag_chain(retriever, prompt, llm):
    """Builds the complete RAG chain with retriever, formatting, prompt, and LLM."""

    try:
        retriever_chain = RunnableMap({"context": lambda inputs: retriever.invoke(inputs["input"]),
                                       "input": lambda inputs: inputs["input"],
                                       "chat_history": lambda inputs: inputs["chat_history"],})

        format_chain = RunnableLambda(lambda x: {**x, "context": format_docs(x["context"])})

        rag_chain = retriever_chain | format_chain | prompt | llm
        
        logger.info("RAG chain constructed.")

        return rag_chain
    
    except Exception as e:
        logger.exception("Failed to build RAG chain.")
        raise ProcessingError("RAG chain build failed.") from e


