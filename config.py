import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    # Database configuration
    
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging configuration
    LOG_DIR = 'logs'
    LOG_FILE = 'app.log'
    LOG_MAX_BYTES = 10240
    LOG_BACKUP_COUNT = 10
    
    # API configuration
    DEBUG = True 