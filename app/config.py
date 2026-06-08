import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # General Configurations
    SECRET_KEY = os.getenv("SECRET_KEY")
    # Database Configurations
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # Disable track modifications to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
