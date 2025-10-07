"""Backwards-compatible CORS configuration."""

from flask import current_app
from flask_cors import CORS


class CORSConfig:
    """CORS configuration that maintains backwards compatibility."""

    @staticmethod
    def get_cors_config(app=None):
        """Get CORS configuration based on environment."""
        # Default to permissive for backwards compatibility
        if app:
            origins = app.config.get("CORS_ORIGINS", "*")
        else:
            origins = "*"

        if origins == "*":
            # Maintain existing wildcard behavior
            return {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": False,
            }
        else:
            # Use configured origins
            return {
                "origins": origins.split(","),
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
            }

    @staticmethod
    def apply_cors(app):
        """Apply CORS configuration to Flask app."""
        config = CORSConfig.get_cors_config(app)
        CORS(
            app,
            resources={
                r"/api/*": config,
                r"/status": config,
                r"/": config,
                r"/graphql": config,
            },
        )

        return app
