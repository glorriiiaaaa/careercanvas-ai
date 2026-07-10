# app/config.py
#
# WHY THIS FILE EXISTS:
# Centralizes all configuration in one place, split by environment.
# Values are pulled from environment variables (.env file) rather than
# hardcoded, so secrets never live in code and settings can differ
# between your laptop (development) and Render (production).

import os
from dotenv import load_dotenv

# Load variables from .env into the actual OS environment
# so os.environ.get() below can see them
load_dotenv()


class Config:
    """
    Base configuration - settings shared across ALL environments.
    Environment-specific classes below inherit from this and override
    only what needs to differ.
    """
    # Used by Flask to sign session cookies and CSRF tokens.
    # Falls back to a placeholder only if .env is somehow missing -
    # we'll make this fail loudly instead once we reach production.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-insecure-key')

    # Disables a SQLAlchemy feature we don't need (event tracking on every
    # DB change) that adds overhead for no benefit in our case.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pulled from .env - the actual PostgreSQL connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentConfig(Config):
    """Used while building on your local machine."""
    DEBUG = True  # Enables detailed error pages and auto-reload on code changes


class ProductionConfig(Config):
    """Used when deployed live on Render. Debug MUST be off here."""
    DEBUG = False


# Maps a simple string name (from .env's FLASK_ENV) to the actual config class.
# This is how create_app() will know which settings to load.
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}