"""Consolidated configuration for the Flask application."""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BaseConfig:
    """Base configuration class with all settings."""

    # Application settings
    APP_NAME = os.environ.get("APP_NAME", "dwml-backend")
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = False
    TESTING = False

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///DudeWheresMyLambo.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis configuration (disabled - using SQLite only)
    # REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

    # API configuration
    API_KEY = os.environ.get("API_KEY")
    KRAKEN_API_URL = os.environ.get(
        "KRAKEN_API_URL", "https://api.kraken.com/0/public/OHLC"
    )

    # CORS configuration
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    # Security configuration
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
    }

    # Rate limiting
    RATE_LIMIT_ENABLED = os.environ.get("RATE_LIMIT_ENABLED", "False").lower() == "true"
    RATE_LIMIT_PER_MINUTE = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "60"))

    # Feature flags
    ENABLE_CACHING = False  # Disabled - no Redis
    ENABLE_MONITORING = os.environ.get("ENABLE_MONITORING", "True").lower() == "true"

    # Performance settings
    REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "30"))
    MAX_WORKERS = int(os.environ.get("MAX_WORKERS", "4"))

    # Logging configuration
    LOG_INFO_FILE = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "log", "info.log"
    )
    LOG_CELERY_FILE = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "log", "celery.log"
    )

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%b %d %Y %H:%M:%S",
            },
            "simple": {"format": "%(levelname)s - %(message)s"},
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "log_info_file": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_INFO_FILE,
                "maxBytes": 16777216,  # 16MB
                "formatter": "standard",
                "backupCount": 5,
            },
        },
        "loggers": {
            APP_NAME: {
                "level": "DEBUG",
                "handlers": ["log_info_file"],
            },
        },
    }

    CELERY_LOGGING = {
        "format": "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s",
        "datefmt": "%b %d %Y %H:%M:%S",
        "filename": LOG_CELERY_FILE,
        "maxBytes": 10000000,  # 10MB
        "backupCount": 5,
    }


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    ENV = "development"


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False
    ENV = "production"
    # Use PostgreSQL in production
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/dwml_production"
    )


# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(environment=None):
    """Get configuration based on environment."""
    if environment is None:
        environment = os.environ.get("FLASK_ENV", "development")

    return config.get(environment, DevelopmentConfig)
