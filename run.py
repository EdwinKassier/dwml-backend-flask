"""This is the core of the api - BACKWARDS COMPATIBLE VERSION
creating a central point for blueprinted frameworks to flow through"""

import json
import os

from app import create_app

# Create app with backwards compatibility
app = create_app()


# Routes are now defined in app/__init__.py to avoid duplication


# NEW: Add backwards-compatible production server support
def run_production_server():
    """Run production server with gunicorn if available."""
    try:
        import gunicorn.app.wsgiapp as wsgi

        wsgi.run()
    except ImportError:
        # Fallback to development server
        app.run(
            port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", debug=False
        )  # FIXED: Disable debug in production


def run_development_server():
    """Run development server with enhanced features."""
    # NEW: Add development-specific configuration
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

    app.run(port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", debug=debug_mode)


if __name__ == "__main__":
    # NEW: Environment-aware server selection
    environment = os.environ.get("FLASK_ENV", "development")

    if environment == "production":
        run_production_server()
    else:
        # PRESERVE: Existing development behavior
        run_development_server()
