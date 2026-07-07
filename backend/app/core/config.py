import os

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings:
    """
    Configuration class to load environment variables.
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

settings = Settings()