"""Flask application factory with simplified structure."""

from typing import Any, Optional

from flask import Flask

# Conditional imports to avoid issues when dependencies are not installed
try:
    from dotenv import load_dotenv

    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

    def load_dotenv(*args: Any, **kwargs: Any) -> None:
        """Placeholder function when dotenv is not available."""
        pass


try:
    from strawberry.flask.views import GraphQLView

    GRAPHQL_AVAILABLE = True
except ImportError:
    GRAPHQL_AVAILABLE = False
    GraphQLView = None  # type: ignore

# Import configuration and extensions
from .config import get_config
from .domain.graphql_schema import schema
from .extensions import init_extensions
from .router import register_routes
from .shared.middleware.cors import CORSConfig
from .shared.middleware.error_handler import register_error_handlers
from .shared.middleware.security import SecurityMiddleware

# Celery disabled - using SQLite only
CELERY_AVAILABLE = False
Celery = None

# Celery disabled - using SQLite only
celery = None


def create_app(environment: Optional[str] = None) -> Flask:
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

    # Register error handlers
    register_error_handlers(app)

    # Celery disabled - using SQLite only
    # if CELERY_AVAILABLE and celery:
    #     celery.config_from_object(app.config, force=True)

    # Register all domain routes
    register_routes(app)

    # Register GraphQL endpoint if available
    if GRAPHQL_AVAILABLE and GraphQLView is not None:
        app.add_url_rule(
            "/graphql",
            view_func=GraphQLView.as_view("graphql_view", schema=schema),
        )

    return app
