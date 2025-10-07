"""Flask application factory with simplified structure."""

from flask import Flask

# Conditional imports to avoid issues when dependencies are not installed
try:
    from dotenv import load_dotenv

    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

    def load_dotenv():
        pass


try:
    from strawberry.flask.views import GraphQLView

    GRAPHQL_AVAILABLE = True
except ImportError:
    GRAPHQL_AVAILABLE = False
    GraphQLView = None

# Import configuration and extensions
from .config import get_config
from .endpoints import crypto_bp, health_bp
from .extensions import init_extensions
from .middleware.cors import CORSConfig
from .middleware.security import SecurityMiddleware
from .schemas import schema

# Celery disabled - using SQLite only
CELERY_AVAILABLE = False
Celery = None

# Celery disabled - using SQLite only
celery = None


def create_app(environment=None):
    """Create Flask application with simplified structure."""

    # Load environment variables if dotenv is available
    if DOTENV_AVAILABLE:
        load_dotenv()

    # Get configuration
    config_class = get_config(environment)
    app = Flask(config_class.APP_NAME)
    app.config.from_object(config_class)

    # Initialize extensions
    init_extensions(app)

    # Apply middleware
    CORSConfig.apply_cors(app)
    app.after_request(SecurityMiddleware.add_security_headers)

    # Celery disabled - using SQLite only
    # if CELERY_AVAILABLE and celery:
    #     celery.config_from_object(app.config, force=True)

    # Register API blueprints
    app.register_blueprint(crypto_bp, url_prefix="/api/v1/project/core")
    app.register_blueprint(health_bp)

    # Register GraphQL endpoint if available
    if GRAPHQL_AVAILABLE and GraphQLView:
        app.add_url_rule(
            "/graphql",
            view_func=GraphQLView.as_view("graphql_view", schema=schema),
        )

    # Add status endpoints
    @app.route("/status", methods=["GET"])
    def status():
        """API status endpoint."""
        return {
            "message": "DudeWheresMyLambo API Status : Running!",
            "version": "1.0.0",
        }, 200

    @app.route("/", methods=["GET"])
    def home():
        """Welcome endpoint."""
        return {"message": "Welcome to the DudeWheresMyLambo API"}, 200

    return app
