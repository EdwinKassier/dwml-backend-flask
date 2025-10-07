"""Health and monitoring endpoints."""

import json
from typing import Tuple

from flask import Blueprint, current_app

health = Blueprint("health", __name__)


@health.route("/health", methods=["GET"])
def health_check() -> Tuple[str, int, dict[str, str]]:
    """Health check endpoint."""
    return (
        json.dumps(
            {"status": "healthy", "service": "dwml-backend", "version": "1.0.0"}
        ),
        200,
        {"Content-Type": "application/json"},
    )


@health.route("/metrics", methods=["GET"])
def metrics() -> Tuple[str, int, dict[str, str]]:
    """Basic metrics endpoint."""
    if not current_app.config.get("ENABLE_MONITORING", True):
        return (
            json.dumps({"message": "Monitoring disabled"}),
            200,
            {"Content-Type": "application/json"},
        )

    # Basic metrics - can be enhanced with Prometheus
    return (
        json.dumps({"uptime": "running", "status": "healthy", "version": "1.0.0"}),
        200,
        {"Content-Type": "application/json"},
    )
