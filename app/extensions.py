"""Flask extensions initialization."""

from typing import Any, Optional

from flask import Flask

# Conditional imports to avoid issues when dependencies are not installed
try:
    from flask_sqlalchemy import SQLAlchemy

    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    SQLAlchemy = None

try:
    from flask_cors import CORS

    CORS_AVAILABLE = True
except ImportError:
    CORS_AVAILABLE = False
    CORS = None

# Celery disabled - using SQLite only
CELERY_AVAILABLE = False
Celery = None

# Initialize extensions only if available
if SQLALCHEMY_AVAILABLE:
    db: Optional[SQLAlchemy] = SQLAlchemy()
else:
    db = None

if CORS_AVAILABLE:
    cors: Optional[CORS] = CORS()
else:
    cors = None

# Celery disabled
celery = None


def init_extensions(app: Flask) -> Flask:
    """Initialize Flask extensions with the app."""
    if SQLALCHEMY_AVAILABLE and db is not None:
        db.init_app(app)

    if CORS_AVAILABLE and cors is not None:
        cors.init_app(app)

    # Celery disabled - no Redis
    # if CELERY_AVAILABLE and celery:
    #     celery.init_app(app)

    return app
