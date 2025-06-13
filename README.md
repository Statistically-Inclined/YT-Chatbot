# 💡 YouBot AI – Talk to YouTube

**Interact with YouTube videos using the power of LLMs and RAG!**
Summarize content, explore viewer opinions, and ask contextual questions about any YouTube video — all from a user-friendly Streamlit interface.


## 🚀 Features

* 🔗 Paste any **YouTube URL**
* 🧠 **Transcript/Subtitles** processed for intelligent summaries
* 💬 **Viewer comments** analyzed for crowd sentiment
* 🎯 Built-in **RAG-based chatbot** to answer questions about the video
* 📥 Option to **download** summaries, Q\&A, comments, and more


## 🖥️ Demo UI Preview


## 🧱 Tech Stack

* **Frontend**: Streamlit
* **LLM & Embeddings**: LangChain + OpenAI / Local models (via `load_model_and_embeddings`)
* **Video Data**: YouTube Data API v3
* **Transcript/Subtitle**: YouTube Transcript API / Subtitle generator
* **RAG Pipeline**: Vector Store + Retriever + Custom Prompt Chain


## 📦 Project Structure

📁 core/
├── config/
│   ├── directory_config.py
│   ├── exceptions.py
│   ├── logger_config.py
│   └── model_config.py
├── document_loader/
│   ├── comment_generator.py
│   ├── metadata_generator.py
│   ├── subtitle_generator.py
│   ├── transcript_generator.py
│   └── url_loader.py
├── comment_summariser/
│   └── runner.py
├── transcript_summariser/
│   └── runner.py
├── rag_pipeline/
│   ├── chain.py
│   ├── prompt.py
│   └── utils.py
├── result_saver/
│   ├── save_comments.py
│   ├── save_metadata.py
│   ├── save_subtitle.py
│   └── save_transcript.py
│
📁 notebook/
│   ├── YT_Chatbot.ipynb
│   ├── YT_Comment.ipynb
│   ├── YT_Streaming.ipynb
│   ├── YT_Summariser.ipynb
│   └── YT_Transcript.ipynb
│
📁 logs/
│   └── app.log
│
📁 output/
├── comments_summary/
│   └── comment_summary.txt
├── transcript_summary/
│   └── transcript_summary.txt
│
📁 youtube_data/
├── comments/
│    ├── comments.txt
│    └── comments.csv
├── metadata/
│    ├── metadata.txt
│    └── metadata.json
├── subtitle/
│    ├── subtitle.txt
│    └── subtitle.json
├── transcript/
│    ├── transcript.txt
│    └── transcript.json
│
├── requirements_base.txt
├── requirements.txt
├── README.md
├── .env
📄 app.py
📄 main.py
📄 test.py

## ⚙️ Setup Instructions

### 1. Clone the Repository

### 2. Install Dependencies

> It's recommended to use a virtual environment.

pip install -r requirements.txt

### 3. Environment Variables

Create a `.env` file at the root with the following variables:

OPENAI_API_KEY=your_openai_key
YOUTUBE_API_KEY=your_youtube_api_key

Ensure these are loaded in your `model_config.py` or relevant files.

### 4. Run the App

streamlit run app.py

## 🧠 How It Works

1. **User inputs** a YouTube URL.
2. **App validates** the URL and extracts the video ID.
3. **YouTube API** fetches metadata and top comments.
4. **Transcript** (or subtitles) are extracted.
5. Summaries are generated for **comments** and **transcript** using LLMs.
6. **RAG pipeline** builds a semantic retriever with vector embeddings.
7. **Chatbot interface** answers user questions using conversational memory.


## 📁 Downloads & Storage

* `transcript.txt / transcript.json`: Saved in `result_saver/`
* `comments.csv / comments.txt`: Top comments
* `metadata.json / .txt`: Video metadata
* `subtitle.txt / .json`: Subtitle fallback
* `chat_history.txt`: Session-based Q\&A


## 🔐 Authentication

Ensure you have valid API keys for:

* **OpenAI** (or another LLM provider)
* **YouTube Data API**


## 📌 Future Improvements

* 🌍 Multilingual support for non-English videos
* 💾 Local file caching for previously analyzed videos
* 🧪 Option to choose between different LLM providers
* 📊 Analytics panel for sentiment over time


## 🤝 Contributing

PRs and feedback are welcome! Feel free to fork and enhance this tool for your use case.


## 📜 License

MIT License – feel free to use, modify, and share.
