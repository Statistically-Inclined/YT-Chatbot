
from langchain.schema.messages import HumanMessage, AIMessage
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError


def run_chat_session(rag_chain):
    """Start an interactive RAG chat session."""

    chat_history = []

    try:
        while True:
            question = input("\n\U0001F9E0 Your Question (type 'exit' to stop): ").strip()
            if question.lower() == "exit":
                logger.info("User exited the chat session.")
                break

            # Invoke the RAG chain and get the response
            response = rag_chain.invoke({"input": question, "chat_history": chat_history})

            print("\n\U0001F916 Answer:", response.content)

            # Update chat history for context
            chat_history.extend([HumanMessage(content=question), AIMessage(content=response.content)])

    except KeyboardInterrupt:
        logger.warning("Chat session interrupted by user.")
        
    except Exception as e:
        logger.exception("Error during chat session.")
        raise ProcessingError("Error occurred during chat session.") from e


