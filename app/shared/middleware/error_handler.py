"""Centralized error handling for API."""

import json
import logging
from typing import Tuple

from flask import Flask

from app.domain.exceptions import (
    ExternalServiceError,
    InsufficientPriceDataError,
    InvalidInvestmentError,
    SymbolNotFoundError,
)

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """
    Register error handlers for the application.

    Args:
        app: Flask application instance
    """

    @app.errorhandler(InvalidInvestmentError)
    def handle_invalid_investment(
        error: InvalidInvestmentError,
    ) -> Tuple[str, int, dict[str, str]]:
        """Handle invalid investment errors."""
        logger.warning(f"Invalid investment: {error}")
        return (
            json.dumps({"error": str(error)}),
            400,
            {"Content-Type": "application/json"},
        )

    @app.errorhandler(SymbolNotFoundError)
    def handle_symbol_not_found(
        error: SymbolNotFoundError,
    ) -> Tuple[str, int, dict[str, str]]:
        """Handle symbol not found errors."""
        logger.warning(f"Symbol not found: {error}")
        return (
            json.dumps({"error": str(error)}),
            404,
            {"Content-Type": "application/json"},
        )

    @app.errorhandler(InsufficientPriceDataError)
    def handle_insufficient_data(
        error: InsufficientPriceDataError,
    ) -> Tuple[str, int, dict[str, str]]:
        """Handle insufficient price data errors."""
        logger.error(f"Insufficient data: {error}")
        return (
            json.dumps({"error": str(error)}),
            503,
            {"Content-Type": "application/json"},
        )

    @app.errorhandler(ExternalServiceError)
    def handle_external_service_error(
        error: ExternalServiceError,
    ) -> Tuple[str, int, dict[str, str]]:
        """Handle external service errors."""
        logger.error(f"External service error: {error}")
        return (
            json.dumps({"error": "Service temporarily unavailable"}),
            503,
            {"Content-Type": "application/json"},
        )

    @app.errorhandler(404)
    def handle_not_found(error: Exception) -> Tuple[str, int, dict[str, str]]:
        """Handle 404 errors."""
        return (
            json.dumps({"error": "Not found"}),
            404,
            {"Content-Type": "application/json"},
        )

    @app.errorhandler(500)
    def handle_internal_error(error: Exception) -> Tuple[str, int, dict[str, str]]:
        """Handle 500 errors."""
        logger.error(f"Internal error: {error}", exc_info=True)
        return (
            json.dumps({"error": "Internal server error"}),
            500,
            {"Content-Type": "application/json"},
        )
