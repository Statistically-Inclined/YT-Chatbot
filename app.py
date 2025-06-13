
import os
import time
import pandas as pd
import streamlit as st
from core.config.logger_config import logger
from core.config.directory_config import COMMENTS_DIR
from core.document_loader.url_loader import get_youtube_video_id_and_url
from core.document_loader.transcript_generator import get_transcript_with_priority
from core.document_loader.subtitle_generator import generate_subtitles_from_youtube_url
from core.config.model_config import load_model_and_embeddings
from core.document_loader.comment_generator import get_video_comments
from core.document_loader.metadata_generator import get_video_metadata
from core.transcript_summariser.runner import run_transcript_summary_chain
from core.comment_summariser.runner import run_comment_summary_chain
from core.rag_pipeline.utils import split_transcript, build_vector_store, get_retriever
from core.rag_pipeline.prompt import build_prompt_template
from core.rag_pipeline.chain import build_rag_chain
from core.result_saver.save_transcript import save_transcript_to_txt, save_transcript_to_json
from core.result_saver.save_comments import save_comments_to_txt, save_comments_to_csv
from core.result_saver.save_metadata import save_metadata_to_text, save_metadata_to_json
from core.result_saver.save_subtitle import save_subtitle_to_json, save_subtitle_to_txt
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from core.config.exceptions import ProcessingError


# Page config
st.set_page_config(page_title="💡 YouBot AI – Talk to YouTube", layout="wide")


# Rag Pipeline Class
class RAGProcessor:
    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.model = None
        self.embedding_model = None
        self.youtube_client = None
        self.rag_chain = None
        self.chat_history: list[BaseMessage] = []


    def initialize_once(self):
        try:
            self.model, self.embedding_model, self.youtube_client = load_model_and_embeddings()
            chunks = split_transcript(self.raw_text)
            vector_store = build_vector_store(chunks, self.embedding_model)
            retriever = get_retriever(vector_store)
            prompt_template = build_prompt_template()
            self.rag_chain = build_rag_chain(retriever, prompt_template, self.model)
        except ProcessingError as pe:
            logger.error(f"Processing Error: {pe}")
            raise pe
        except Exception as e:
            logger.exception(f"Unexpected error during initialization: {e}")
            raise e


    def answer_question(self, question: str) -> str:
        try:
            if not self.rag_chain:
                raise ValueError("RAG pipeline not initialized. Call `initialize_once()` first.")
            
            logger.info(f"Question: {question}")

            response = self.rag_chain.invoke({"input": question, "chat_history": self.chat_history})
            self.chat_history.extend([HumanMessage(content=question), AIMessage(content=response.content)])
            self.chat_history = self.chat_history[-3:]

            logger.info(f"Answer: {response.content}")
            logger.info(f"Chat History: {self.chat_history}")

            return response.content
        
        except Exception as e:
            logger.exception("Error while answering question.")
            return "Something went wrong while answering the question."


# Session state initialization
for key in ["processor", "chat_history", "video_processed", "metadata", 
            "comments_df", "summary_transcript", "summary_comments", "raw_text", "url"]:
    
    if key not in st.session_state:
        st.session_state[key] = None if key != "chat_history" else []


# Header
st.title("🎬➡️🧠 YouBot AI – YouTube Q&A Assistant")


# Sub-Header
st.markdown("""
👋 **Welcome to YouBot AI!**  

- 🔗 Enter a YouTube video URL
- 🧬 Receive a concise summary of the content
- 🧑‍🤝‍🧑 Explore key audience perspectives
- 📚 Ask questions and get contextual answers
""")


## Typing Effect... word by word!
def typing_effect(placeholder, text, delay=0.05, hold_time=2):
    typed = ""
    for char in text:
        typed += char
        placeholder.info(typed)
        time.sleep(delay)
    time.sleep(hold_time)


## Deleting Effect... word by word!
def deleting_effect(placeholder, text, delay=0.05):
    for i in range(len(text), 0, -1):
        placeholder.info(text[:i])
        time.sleep(delay)
    placeholder.info("\u00A0") 


# Input UI
st.sidebar.markdown("🎬 Enter YouTube URL")

# Submit Button & Enter Key Both will Trigger the Process
with st.sidebar.form(key="video_form"):
    url_input = st.text_input("🔗 YouTube Video Link", placeholder="e.g., https://www.youtube.com/watch?v=abc123")
    submit = st.form_submit_button("🚀 Process Video", use_container_width=True)


# Processing block
if submit and url_input:
    
    st.session_state.url = url_input

    status_placeholder = st.empty()
    typing_effect(status_placeholder, "🔎 Validating YouTube URL & Extracting Video ID")

    video_id, valid_url = get_youtube_video_id_and_url(url_input)
    
    deleting_effect(status_placeholder, "🔎 Validating YouTube URL & Extracting Video ID")
    typing_effect(status_placeholder, "⚙️ Initializing LLM, Embedding Model, and YouTube API Client")

    llm_model, embedding_model, youtube_client = load_model_and_embeddings()

    # Metadata
    deleting_effect(status_placeholder, "⚙️ Initializing LLM, Embedding Model, and YouTube API Client")
    typing_effect(status_placeholder, "📋 Fetching Video Metadata using the YouTube API Client")

    metadata = get_video_metadata(youtube_client, video_id)
    save_metadata_to_text(metadata)
    save_metadata_to_json(metadata)

    # Comments
    deleting_effect(status_placeholder, "📋 Fetching Video Metadata using the YouTube API Client")
    typing_effect(status_placeholder, "💬  Retrieving Top Viewer Comments using the YouTube API Client")

    comments = get_video_comments(youtube_client, video_id)
    save_comments_to_txt(comments)
    save_comments_to_csv(comments)
    
    df = pd.read_csv(os.path.join(COMMENTS_DIR, 'comments.csv'))
    
    deleting_effect(status_placeholder, "💬  Retrieving Top Viewer Comments using the YouTube API Client")
    typing_effect(status_placeholder, "🧠 Summarizing Audience Opinions & Key Discussion Points")

    # Comment Summary
    summary_comments = run_comment_summary_chain(llm_model, comments, video_id, max_comments=20)

    # Transcript / Subtitles
    deleting_effect(status_placeholder, "🧠 Summarizing Audience Opinions & Key Discussion Points")
    typing_effect(status_placeholder, "📄 Retrieving & Processing the Video’s Transcript or Subtitles")
        
    try:
        deleting_effect(status_placeholder, "📄 Retrieving & Processing the Video’s Transcript or Subtitles")
        typing_effect(status_placeholder, "🎙️ Attempting to Generate Summary using the Transcript")

        transcript_chunks, transcript = get_transcript_with_priority(69, video_id)
        raw_text = transcript
        save_transcript_to_txt(transcript_chunks)
        save_transcript_to_json(transcript_chunks)

        deleting_effect(status_placeholder, "🎙️ Attempting to Generate Summary using the Transcript")
        typing_effect(status_placeholder, "🧠 Generating an Intelligent Summary from the Extracted Context")

    except:
        deleting_effect(status_placeholder, "📄 Retrieving & Processing the Video’s Transcript or Subtitles")
        typing_effect(status_placeholder, "🎙️ Attempting to Generate Summary using the Subtitles")

        text, text_timestamp = generate_subtitles_from_youtube_url(valid_url)
        save_subtitle_to_json(text_timestamp)
        save_subtitle_to_txt(text)
        raw_text = text

        deleting_effect(status_placeholder, "🎙️ Attempting to Generate Summary using the Subtitles")
        typing_effect(status_placeholder, "🧠 Generating an Intelligent Summary from the Extracted Context")
   
    # Transcript or Subtitle Summary
    summary_transcript = run_transcript_summary_chain(llm_model, raw_text)

    deleting_effect(status_placeholder, "🧠 Generating an Intelligent Summary from the Extracted Context")
    typing_effect(status_placeholder, "🧠 Building Semantic Memory: Vector Store and Retriever Initialized")

    # Store in session
    st.session_state.update({
        "video_processed": True,
        "metadata": metadata,
        "comments_df": df,
        "summary_comments": summary_comments,
        "summary_transcript": summary_transcript,
        "raw_text": raw_text,
        "rag_chain": st.session_state.get("rag_chain") or 
                     build_rag_chain(get_retriever(build_vector_store(split_transcript(raw_text), 
                                                                      embedding_model)), 
                                                                      build_prompt_template(), llm_model),
        "processor": RAGProcessor(raw_text)
    })
    
    deleting_effect(status_placeholder, "🧠 Building Semantic Memory: Vector Store and Retriever Initialized")
    typing_effect(status_placeholder, "⚙️ Initializing the Retrieval-Augmented Generation (RAG) Engine")

    st.session_state.processor.initialize_once()

    deleting_effect(status_placeholder, "⚙️ Initializing the Retrieval-Augmented Generation (RAG) Engine")
    typing_effect(status_placeholder, "✅ Setup complete — YouBot is ready to assist you! 🎉")

    status_placeholder.empty()


# After Video Processed
if st.session_state.get("video_processed"):

    st.markdown("**✅ Setup complete. YouBot is ready to assist you!**")

    metadata = st.session_state.metadata
    df = st.session_state.comments_df
    summary_transcript = st.session_state.summary_transcript
    summary_comments = st.session_state.summary_comments

    # Start the Video
    st.video(st.session_state.url)

    # Sidebar info
    st.sidebar.markdown(f"**🎬 Title:** {metadata.get('title', 'N/A')}")
    st.sidebar.markdown(f"**📅 Published On:** {metadata.get('published_at', 'N/A')}")
    st.sidebar.markdown(f"**📺 Channel:** {metadata.get('channel_title', 'N/A')}")
    st.sidebar.markdown(f"**🆔 Video ID:** `{metadata.get('video_id', 'N/A')}`")
    st.sidebar.markdown(f"**💬 Comments:** {metadata.get('comment_count', 'N/A')}")
    st.sidebar.markdown(f"**👁️ Views:** {metadata.get('view_count', 'N/A')}")
    st.sidebar.markdown(f"**👍 Likes:** {metadata.get('like_count', 'N/A')}")


    # Left Column Content, Split Screen in 1:1
    left_col, right_col = st.columns([1, 1])  

    with left_col:

        st.markdown("### 🧭 Quick Explore")

        with st.expander("🎬 About the Video"):
            st.markdown( f"<div style='text-align: justify;'>{metadata.get('description', 'No description available.')}</div>", unsafe_allow_html=True)

        with st.expander("🌟 Top Comments"):
            st.dataframe(df[['author', 'text']], hide_index=True)

        with st.expander("💡 Comment Insights", expanded=False):
            st.markdown("#### 🧑‍🤝‍🧑 What Viewers Are Saying")
            st.write(summary_comments)

            st.download_button(label="💾 Download Comment Insights", data=summary_comments, file_name="comment_insights.txt", mime="text/plain")

        with st.expander("🎯 Smart Summary", expanded=True):
            st.markdown("#### ✍️ Key Takeaways")
            st.write(summary_transcript)

            st.download_button(label="💾 Download Summary", data=summary_transcript, file_name="video_summary.txt", mime="text/plain")


else:
    # Ensure consistent layout
    left_col, right_col = st.columns([1, 1])  


# Right column content (Chatbot) - Always outside the conditional
# Split Screen in 1:1
with right_col:
    if st.session_state.processor:
        st.markdown("### 🎙️ Talk to the Video")

        with st.form("query_form", clear_on_submit=True):
            query = st.text_input("Ask Anything...", placeholder="e.g. What’s the video about?", key="query_input")
            submitted = st.form_submit_button("🚀 Ask YouBot")

        if submitted and query:

            with st.spinner("💭 Cooking up an answer...."):
                result = st.session_state.processor.answer_question(query)

            st.session_state.chat_history.append((query, result))

            if len(st.session_state.chat_history) > 5:
                st.session_state.chat_history.pop(0)

            st.success("✅ Answer Ready!")
            st.markdown(f"**🗨️ Question:** `{query}`")
            st.markdown(f"**🧠 Answer:**\n\n{result}")

            # Prepare Q&A text for download
            qa_text = f"Question: {query}\nAnswer: {result}"
            st.download_button(label="💾 Download Q&A", data=qa_text, file_name="youbot_qa.txt", mime="text/plain")


    if st.session_state.chat_history:
        st.markdown("### 🔖 Recent Questions")
        for i, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
            with st.expander(f"🔹 Q{i}: {q}"):
                st.markdown(f"**🧠 Answer:** {a}")
        
        # Combine all Q&A into one text block
        history_text = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.chat_history])
        st.download_button(label="💾 Download Chat History", data=history_text, file_name="youbot_chat_history.txt", mime="text/plain")
 
