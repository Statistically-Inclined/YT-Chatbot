
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from core.config.logger_config import logger
from core.config.exceptions import ProcessingError, ResourceNotFoundError
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


def load_model_and_embeddings():
    
    try:
        load_dotenv(override=True)

        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        if not youtube_api_key:
            raise ResourceNotFoundError("❌ YOUTUBE_API_KEY not found in .env file")

        logger.info("YouTube API key loaded successfully.")

        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ResourceNotFoundError("❌ GOOGLE_API_KEY is missing from the environment.")

        logger.info("Google API key loaded successfully.")

        youtube_client = build("youtube", "v3", developerKey=youtube_api_key, cache_discovery=False)
        logger.info("YouTube API client initialized.")

        llm_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5, max_tokens=1000)
        logger.info("Gemini model loaded successfully.")

        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        logger.info("Embedding model loaded successfully.")

        return llm_model, embedding_model, youtube_client

    except Exception as e:
        
        logger.exception("Failed to initialize models or API clients.")
        raise ProcessingError("Model or embedding initialization failed.") from e
