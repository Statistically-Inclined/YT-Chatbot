import streamlit as st

st.title("🎬 YouTube Video Player")

# Input for YouTube URL
video_url = st.text_input("Enter a YouTube video URL:")

# Stream video if a valid URL is entered
if video_url:
    st.video(video_url)
