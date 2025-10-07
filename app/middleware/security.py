"""Backwards-compatible security middleware."""

from flask import request, current_app
from functools import wraps


class SecurityMiddleware:
    """Security middleware that adds security headers without breaking existing
    functionality."""

    @staticmethod
    def add_security_headers(response):
        """Add security headers to responses without breaking existing behavior."""
        # Only add headers if not already present (backwards compatible)
        if "X-Content-Type-Options" not in response.headers:
            response.headers["X-Content-Type-Options"] = "nosniff"

        if "X-Frame-Options" not in response.headers:
            response.headers["X-Frame-Options"] = "DENY"

        if "X-XSS-Protection" not in response.headers:
            response.headers["X-XSS-Protection"] = "1; mode=block"

        # Add feature flag header for gradual rollout
        response.headers["X-API-Version"] = "1.0"
        response.headers["X-Feature-Flags"] = "security-headers"

        return response

    @staticmethod
    def validate_input(symbol, investment):
        """Validate input parameters while preserving existing behavior."""
        # Preserve existing behavior: convert to string and strip
        symbol = str(symbol).strip() if symbol else ""
        investment = int(investment) if investment else 0

        # Add validation without breaking existing logic
        if not symbol:
            raise ValueError("Symbol parameter is required")

        if investment <= 0:
            raise ValueError("Investment must be a positive integer")

        return symbol, investment

    @staticmethod
    def log_request():
        """Log requests for security monitoring without affecting performance."""
        if current_app.config.get("ENABLE_MONITORING", True):
            current_app.logger.info(
                f"Request: {request.method} {request.path} "
                f"from {request.remote_addr} "
                f"User-Agent: {request.headers.get('User-Agent', 'Unknown')}"
            )


def security_enhanced_route(original_route):
    """Decorator that enhances existing routes with security features."""

    @wraps(original_route)
    def wrapper(*args, **kwargs):
        # Log the request
        SecurityMiddleware.log_request()

        # Call the original route
        return original_route(*args, **kwargs)

    return wrapper
