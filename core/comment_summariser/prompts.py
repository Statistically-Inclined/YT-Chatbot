
from langchain.prompts import PromptTemplate
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.prompts.comments import comment_map_prompt, comment_combine_prompt


def build_comment_prompt_templates():
    """Prepare prompt templates for map-reduce summarization of comments."""

    try:
        map_template = PromptTemplate(input_variables=['text'], template=comment_map_prompt)
        combine_template = PromptTemplate(input_variables=['text'], template=comment_combine_prompt)

        logger.info("Built comment summarization prompt templates.")

        return map_template, combine_template
    
    except Exception as e:
        logger.exception("Failed to build prompt templates.")
        raise ProcessingError("Prompt template creation failed.") from e
