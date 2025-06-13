
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


llm_model, embedding_model, youtube_client = load_model_and_embeddings()

url = "https://www.youtube.com/watch?v=5sLYAQS9sWQ"
video_id, valid_url = get_youtube_video_id_and_url(url)
print(f"Video ID: {video_id}, URL: {valid_url}")

# Transcript or Subtitle Loading

# # OPTION 1: Transcript-based RAG
# transcript_chunks, transcript = get_transcript_with_priority(video_id)
# save_transcript_to_txt(transcript_chunks, filename="transcript.txt")
# save_transcript_to_json(transcript, filename="transcript.json")
# raw_text = transcript  # Use transcript for RAG input


# OPTION 2: Subtitle-based RAG (Recommended fallback)
text, text_timestamp = generate_subtitles_from_youtube_url(valid_url)
save_subtitle_to_json(text_timestamp)
save_subtitle_to_txt(text)
raw_text = text  # Use subtitle text for RAG input


# Save Comments & Metadata
comments = get_video_comments(youtube_client, video_id)
save_comments_to_csv(comments)
save_comments_to_txt(comments)

metadata = get_video_metadata(youtube_client, video_id)
save_metadata_to_json(metadata)
save_metadata_to_text(metadata)


# Generate Transcript Summary
run_transcript_summary_chain(llm_model, raw_text)

# Generate Comment Summary
run_comment_summary_chain(llm_model, youtube_client, video_id)


# Vector Store & RAG Setup

# Step 1: Split into chunks
chunks = split_transcript(raw_text)

# Step 2: Build vector store
vector_store = build_vector_store(chunks, embedding_model)

# Step 3: Create retriever
retriever = get_retriever(vector_store)

# Step 4: Build prompt template
prompt_template = build_prompt_template()

# Step 5: Construct RAG chain
rag_chain = build_rag_chain(retriever, prompt_template, llm_model)

# Step 6: Run the chat session
run_chat_session(rag_chain)
