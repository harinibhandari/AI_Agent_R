"""
Configuration settings for the application.
Loads environment variables from the .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL", "llama-3.3-70b-versatile")


def validate_config():
    """
    Validate required configuration values.
    """
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. Please add it to your .env file."
        )