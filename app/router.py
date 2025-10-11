"""Root router - registers all domain endpoints."""

import json
from datetime import UTC, datetime
from typing import Tuple

from flask import Blueprint, Flask

from app.domain.routes import crypto_bp

# Create health blueprint at root level
health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check() -> Tuple[str, int, dict[str, str]]:
    """
    Health check endpoint.

    Returns:
        JSON indicating service health
    """
    return (
        json.dumps(
            {
                "status": "healthy",
                "service": "dwml-backend",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        ),
        200,
        {"Content-Type": "application/json"},
    )


def register_routes(app: Flask) -> None:
    """
    Register all domain routes with the Flask app.

    Currently two domains:
    - domain: Main DWML application endpoints (process_request, etc.)
    - shared: Shared functionality between domains

    Args:
        app: Flask application instance
    """
    # Register main domain routes
    app.register_blueprint(crypto_bp, url_prefix="/api/v1")

    # Register health check
    app.register_blueprint(health_bp)

    # Add status endpoints
    @app.route("/status", methods=["GET"])
    def status() -> tuple[dict[str, str], int]:
        """API status endpoint."""
        return {
            "message": "DudeWheresMyLambo API Status : Running!",
            "version": "1.0.0",
        }, 200

    @app.route("/", methods=["GET"])
    def home() -> tuple[dict[str, str], int]:
        """Welcome endpoint."""
        return {"message": "Welcome to the DudeWheresMyLambo API"}, 200
