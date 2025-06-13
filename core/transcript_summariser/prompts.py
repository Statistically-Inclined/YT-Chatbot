
from langchain.prompts import PromptTemplate
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.prompts.transcript import transcript_map_prompt, transcript_combine_prompt


def build_transcript_prompt_templates():
    """Builds prompt templates for map and reduce summarization."""

    try:
        map_prompt_template = PromptTemplate(input_variables=['text'], template=transcript_map_prompt)
        combine_prompt_template = PromptTemplate(input_variables=['text'], template=transcript_combine_prompt)

        logger.info("Map and combine prompt templates created.")

        return map_prompt_template, combine_prompt_template
    
    except Exception as e:
        logger.exception("Failed to build summarization prompt templates.")
        raise ProcessingError("Prompt template building failed.") from e