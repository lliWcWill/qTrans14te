import os
import logging
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# API Keys - Handle both local env and Streamlit Cloud secrets
try:
    # Try Streamlit secrets first (for cloud deployment)
    GROQ_API_KEY = st.secrets.get('GROQ_API_KEY', os.getenv('GROQ_API_KEY'))
    ELEVEN_LABS_API_KEY = st.secrets.get('ELEVEN_LABS_API_KEY', os.getenv('ELEVEN_LABS_API_KEY'))
except:
    # Fall back to environment variables (for local development)
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    ELEVEN_LABS_API_KEY = os.getenv('ELEVEN_LABS_API_KEY')

# Logging Configuration
def setup_logging():
    """Setup logging configuration for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    
    loggers = {
        'api': logging.getLogger('api'),
        'transcription': logging.getLogger('transcription'),
        'ui': logging.getLogger('ui'),
        'audio': logging.getLogger('audio')
    }
    
    return loggers

# Initialize loggers
LOGGERS = setup_logging()