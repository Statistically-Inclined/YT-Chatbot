
from core.document_loader.url_loader import get_youtube_video_id_and_url
from core.document_loader.transcript_generator import get_transcript_with_priority
from core.document_loader.subtitle_generator import generate_subtitles_from_youtube_url
from core.config.model_config import load_model_and_embeddings
from core.document_loader.comment_generator import get_video_comments
from core.document_loader.metadata_generator import get_video_metadata
from core.result_saver.save_transcript import save_transcript_to_json, save_transcript_to_txt
from core.result_saver.save_comments import save_comments_to_csv, save_comments_to_txt
from core.result_saver.save_metadata import save_metadata_to_json, save_metadata_to_text
from core.result_saver.save_subtitle import save_subtitle_to_json, save_subtitle_to_txt
from core.rag_pipeline.utils import split_transcript, build_vector_store, get_retriever
from core.rag_pipeline.prompt import build_prompt_template
from core.rag_pipeline.chain import build_rag_chain
from core.rag_pipeline.session import run_chat_session
from core.transcript_summariser.runner import run_transcript_summary_chain
from core.comment_summariser.runner import run_comment_summary_chain
from core.config.logger_config import logger

def main():
    try:
        llm_model, embedding_model, youtube_client = load_model_and_embeddings()

        url = "https://www.youtube.com/watch?v=5sLYAQS9sWQ"
        video_id, valid_url = get_youtube_video_id_and_url(url)
        logger.info(f"Video ID: {video_id}, URL: {valid_url}")

        raw_text = load_transcript_or_subtitle(video_id, valid_url)
        save_comments_and_metadata(youtube_client, video_id)

        run_transcript_summary_chain(llm_model, raw_text)
        run_comment_summary_chain(llm_model, youtube_client, video_id)

        run_rag_pipeline(raw_text, embedding_model, llm_model)

    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")


def load_transcript_or_subtitle(video_id, url):
    try:
        transcript_chunks, transcript = get_transcript_with_priority(video_id)
        save_transcript_to_txt(transcript_chunks, filename="transcript.txt")
        save_transcript_to_json(transcript_chunks, filename="transcript.json")
        logger.info("Transcript successfully retrieved and saved.")
        return transcript
    
    except Exception as e:
        logger.warning(f"Transcript failed, falling back to subtitles: {e}")
        text, text_timestamp = generate_subtitles_from_youtube_url(url)
        save_subtitle_to_json(text_timestamp)
        save_subtitle_to_txt(text)
        logger.info("Subtitles successfully retrieved and saved.")
        return text


def save_comments_and_metadata(client, video_id):
    try:
        comments = get_video_comments(client, video_id)
        save_comments_to_csv(comments)
        save_comments_to_txt(comments)
        logger.info("Comments saved successfully.")

    except Exception as e:
        logger.warning(f"Failed to retrieve/save comments: {e}")

    try:
        metadata = get_video_metadata(client, video_id)
        save_metadata_to_json(metadata)
        save_metadata_to_text(metadata)
        logger.info("Metadata saved successfully.")

    except Exception as e:
        logger.warning(f"Failed to retrieve/save metadata: {e}")


def run_rag_pipeline(raw_text, embedding_model, llm_model):
    try:
        chunks = split_transcript(raw_text)
        vector_store = build_vector_store(chunks, embedding_model)
        retriever = get_retriever(vector_store)
        prompt_template = build_prompt_template()
        rag_chain = build_rag_chain(retriever, prompt_template, llm_model)

        run_chat_session(rag_chain)
        logger.info("RAG chat session completed successfully.")

    except Exception as e:
        logger.error(f"RAG pipeline failed: {e}")



if __name__ == "__main__":
    main()
