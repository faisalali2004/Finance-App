# config.py

import os

class Config:
    """Base configuration for the Flask application."""
    # SECRET_KEY is used for session management and security,
    # it should be a long, random string.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_very_secure_random_secret_key_here_for_development'

    # SQLALCHEMY_DATABASE_URI specifies the database connection string.
    # It attempts to use an environment variable (e.g., for production databases)
    # and falls back to a local SQLite database for development.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'

    # SQLALCHEMY_TRACK_MODIFICATIONS set to False to disable Flask-SQLAlchemy event system,
    # which saves memory and is recommended.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration, inheriting from base Config."""
    # DEBUG mode provides interactive debugger for development.
    # Should always be False in production.
    DEBUG = True
    # You might add development-specific settings here, e.g., less strict logging

class ProductionConfig(Config):
    """Production configuration, inheriting from base Config."""
    DEBUG = False
    # Add production-specific settings here, e.g.,:
    # SQLALCHEMY_DATABASE_URI for a production database (PostgreSQL, MySQL, etc.)
    # LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # More robust error logging setup
    # Email settings for error reporting
