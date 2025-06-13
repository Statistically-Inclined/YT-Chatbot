
from langchain.chains.summarize import load_summarize_chain
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.comment_summariser.utils import split_comments_to_summary
from core.comment_summariser.prompts import build_comment_prompt_templates
from core.result_saver.save_summary import save_comment_summary_to_txt


def run_comment_summary_chain(llm, comments, video_id: str, max_comments: int = 50) -> str:
    """Main function to fetch, chunk, and summarize video comments."""

    try:
        # Processing comments from YouTube API
        comment_texts = [c["text"] for c in comments]

        # Split comments into chunks for processing
        chunks = split_comments_to_summary(comment_texts)

        # Load the summarization prompt templates
        map_prompt, combine_prompt = build_comment_prompt_templates()

        # Load and run the summarization chain
        summary_chain = load_summarize_chain(llm=llm, 
                                             chain_type='map_reduce',
                                             map_prompt=map_prompt,
                                             combine_prompt=combine_prompt,
                                             verbose=False)

        # Run the summarization chain
        output = summary_chain.invoke(chunks)
        final_summary = output['output_text']
        
        logger.info("Comment Summarization completed.")

        # Save the summary to output file
        saved_path = save_comment_summary_to_txt(final_summary, base_filename='Comment_Summary')
        logger.info(f"Summary written to file: {saved_path}")

        return final_summary
    
    except Exception as e:
        logger.exception("Failed to summarize video comments.")
        raise ProcessingError("Video comment summarization failed.") from e
