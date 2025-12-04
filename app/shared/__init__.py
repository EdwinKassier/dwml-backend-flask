"""Shared domain components."""

# Import tasks for Celery autodiscovery
try:
    from . import tasks  # noqa: F401
except ImportError:
    # Celery might not be available
    pass

from .database import Database

shared_db = Database()
