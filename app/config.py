import os

class Config:
    """Basic configuration class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Used for encrypted sessions and other security features
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'your_default_salt')  # For password hashing
    DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Whether to enable debug mode

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')  # Default URI for SQLite databases
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable object change tracking to save memory

    # Mail configuration (if you need to send emails)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.example.com')  # Mail Server
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Mail server port
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'  # Whether to use TLS
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Email Username
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Email Password
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@example.com')  # Default Sender

# Using the Configuration Class in Your Application
# from config import Config
# app.config.from_object(Config)
