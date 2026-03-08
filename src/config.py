"""
Configuration settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    @classmethod
    def validate(cls):
        """Validate that required configuration variables are set"""
        required = {
            "GOOGLE_SHEET_ID": cls.GOOGLE_SHEET_ID,
            "GOOGLE_CREDENTIALS_PATH": cls.GOOGLE_CREDENTIALS_PATH,
            "OPENAI_API_KEY": cls.OPENAI_API_KEY,
        }
        
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}. Please check your .env file.")
        
        # Check if credentials file exists
        if not os.path.exists(cls.GOOGLE_CREDENTIALS_PATH):
            raise FileNotFoundError(f"Credentials file not found at: {cls.GOOGLE_CREDENTIALS_PATH}")