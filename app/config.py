import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask application key
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail server configuration (optional)
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # Other configurations
    DEBUG = os.getenv('DEBUG', 'false').lower() in ['true', 'on', '1']