
from langchain.chains.summarize import load_summarize_chain
from core.transcript_summariser.utils import split_transcript_for_summary
from core.transcript_summariser.prompts import build_transcript_prompt_templates
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError
from core.result_saver.save_summary import save_transcript_summary_to_txt


def run_transcript_summary_chain(llm, transcript: str):
    """Runs map-reduce summarization chain and saves the final summary."""
    try:
        # Step 1: Split transcript into manageable chunks
        chunks = split_transcript_for_summary(transcript)

        # Step 2: Prepare map and combine prompts
        map_prompt, combine_prompt = build_transcript_prompt_templates()

        # Step 3: Load summarization chain using map-reduce strategy
        summary_chain = load_summarize_chain(llm=llm,
                                             chain_type='map_reduce',
                                             map_prompt=map_prompt,
                                             combine_prompt=combine_prompt,
                                             verbose=False)
        
        logger.info("Summarization chain loaded with map-reduce strategy.")

        # Step 4: Run the summarization chain
        output = summary_chain.invoke(chunks)
        final_summary = output['output_text']
        
        logger.info("Summarization completed.")

        # Step 5: Save the summary to output file
        saved_path = save_transcript_summary_to_txt(final_summary, base_filename='Transcript_Summary')
        logger.info(f"Summary written to file: {saved_path}")

        return final_summary
    
    except Exception as e:
        logger.exception("Failed to run summarization chain.")
        raise ProcessingError("Summarization failed.") from e