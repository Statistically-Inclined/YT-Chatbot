
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.prompts.chatbot import chatbot_prompt


def build_prompt_template():
    """Constructs the chat prompt template using system and user messages."""

    try:
        template = chatbot_prompt
        prompt = ChatPromptTemplate.from_messages([MessagesPlaceholder(variable_name="chat_history"),
                                                   ("system", template), 
                                                   ("human", "question:{input}")])
        logger.info("Prompt template created.")

        return prompt
    
    except Exception as e:
        logger.exception("Failed to build prompt template.")
        raise ProcessingError("Prompt template creation failed.") from e


