"""Celery application factory for background tasks.

This module provides a proper Celery factory pattern that integrates
with Flask application context to ensure tasks can access Flask features.
"""

import logging
from typing import Optional

from celery import Celery
from flask import Flask

logger = logging.getLogger(__name__)


def create_celery_app(app: Optional[Flask] = None) -> Celery:
    """
    Create and configure Celery application.

    This factory pattern properly integrates Celery with Flask,
    ensuring tasks run within the Flask application context.

    Args:
        app: Flask application instance (optional)

    Returns:
        Configured Celery instance
    """
    celery = Celery(
        app.import_name if app else "app",
        broker=(
            app.config.get("CELERY_BROKER_URL") if app else "redis://localhost:6379/0"
        ),
        backend=(
            app.config.get("CELERY_RESULT_BACKEND")
            if app
            else "redis://localhost:6379/0"
        ),
        include=["app.domain.tasks", "app.shared.tasks"],  # Auto-discover tasks
    )

    if app:
        # Update Celery config from Flask app
        celery.conf.update(app.config)

        # Configure Celery settings
        celery.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            enable_utc=True,
            task_track_started=True,
            task_time_limit=300,  # 5 minutes
            task_soft_time_limit=270,  # 4.5 minutes
            task_acks_late=True,
            worker_prefetch_multiplier=1,
            result_expires=3600,  # 1 hour
            result_persistent=True,
            broker_connection_retry_on_startup=True,
            broker_connection_retry=True,
            broker_connection_max_retries=10,
        )

        # Ensure tasks run within Flask app context
        class ContextTask(celery.Task):
            """Task with Flask application context."""

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery.Task = ContextTask

        logger.info("Celery app configured successfully")

    return celery
