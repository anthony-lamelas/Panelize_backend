import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Flask Configuration
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False
    
    # CORS Configuration
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'https://panelize-frontend.onrender.com').split(',')
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        return True

