"""Celery worker entry point.

This module creates a Celery application instance that can be used
to run workers, beat scheduler, and other Celery components.

Usage:
    # Start worker
    celery -A celery_worker.celery worker --loglevel=info

    # Start beat scheduler
    celery -A celery_worker.celery beat --loglevel=info

    # Start flower monitoring
    celery -A celery_worker.celery flower
"""

import os

# Set up environment before importing Flask app
if not os.environ.get("FLASK_ENV"):
    os.environ["FLASK_ENV"] = "development"

from app import create_app

# Create Flask app instance
app = create_app(os.getenv("FLASK_ENV"))

# Get Celery instance from Flask app
celery = app.celery

# Ensure tasks are discoverable
# Tasks are auto-discovered via the include parameter in celery_app.py
# and the imports in domain/__init__.py and shared/__init__.py

if __name__ == "__main__":
    # This allows running the worker with: python celery_worker.py
    # But typically you'd use: celery -A celery_worker.celery worker
    celery.start()
