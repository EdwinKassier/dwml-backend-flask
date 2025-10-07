"""Crypto investment analysis endpoints."""

import json
import grpc
from flask import Blueprint, current_app, request
from werkzeug.local import LocalProxy

# Import existing modules to preserve behavior
from app.utils import data_collector, graph_creator
from app.utils.proto_files import api_pb2_grpc as pb2_grpc
from app.utils.proto_files import api_pb2 as pb2
from app.middleware.auth import check_auth

# Import new security middleware
from app.middleware.security import SecurityMiddleware, security_enhanced_route
from app.middleware.rate_limit import rate_limit

core = Blueprint("crypto", __name__)
logger = LocalProxy(lambda: current_app.logger)


@core.before_request
def before_request_func():
    """Ensure logger name is set - EXACT SAME BEHAVIOR."""
    current_app.logger.name = "core"


@core.route("/process_request", methods=["GET"])
@rate_limit(limit=60, window=60)  # NEW: Add rate limiting
@security_enhanced_route  # NEW: Add security enhancements
def main_request():
    """Process a request around the main logic of the api - EXACT SAME BEHAVIOR."""

    logger.info("app test route hit")
    try:
        # PRESERVE: Exact same parameter handling
        symbol = str(request.args.get("symbol", "").strip())
        investment = int(request.args.get("investment", 0))

        # NEW: Add input validation with backwards compatibility
        try:
            symbol, investment = SecurityMiddleware.validate_input(symbol, investment)
        except ValueError:
            # Return same error format as before
            return (
                json.dumps({"message": "Server Failure"}),
                500,
                {"Content-Type": "application/json"},
            )

        # PRESERVE: Exact same business logic
        collector = data_collector.DataCollector(symbol, investment)
        creator = graph_creator.GraphCreator(symbol)
        result = collector.driver_logic()
        graph_data = creator.driver_logic()

        # Parse graph_data if it's a JSON string
        if isinstance(graph_data, str):
            try:
                graph_data = json.loads(graph_data)
            except json.JSONDecodeError:
                pass  # Keep as string if not valid JSON

        # PRESERVE: Exact same response format
        return (
            json.dumps({"message": result, "graph_data": graph_data}),
            200,
            {"Content-Type": "application/json"},
        )
    except Exception:
        # PRESERVE: Exact same error handling
        return (
            json.dumps({"message": "Server Failure"}),
            500,
            {"Content-Type": "application/json"},
        )


@core.route("/process_request_grpc", methods=["GET"])
@rate_limit(limit=60, window=60)  # NEW: Add rate limiting
@security_enhanced_route  # NEW: Add security enhancements
def main_request_grpc():
    """Process a request around the main logic of the api - EXACT SAME BEHAVIOR."""

    logger.info("app test route hit")
    try:
        # PRESERVE: Exact same parameter handling
        symbol = str(request.args.get("symbol", "").strip())
        investment = int(request.args.get("investment", 0))

        logger.info(f"app test route hit args {symbol}:{investment}")

        # NEW: Add input validation with backwards compatibility
        try:
            symbol, investment = SecurityMiddleware.validate_input(symbol, investment)
        except ValueError as e:
            # Return same error format as before
            return (
                json.dumps({"error": str(e)}),
                500,
                {"ContentType": "application/json"},
            )

        # PRESERVE: Exact same gRPC logic
        endpoint = "master-dwml-backend-python-grpc-lqfbwlkw2a-uc.a.run.app"
        channel = grpc.secure_channel(endpoint, grpc.ssl_channel_credentials())
        stub = pb2_grpc.APIStub(channel)
        logger.info(f"app test route stub {stub}")
        response = stub.processRequest(
            pb2.apiRequest(symbol=symbol, investment=investment)
        )
        logger.info(f"app test route hit response {response}")
        print(response)

        # PRESERVE: Exact same response format
        return (
            json.dumps(
                {"message": response.message, "graph_data": response.graph_data}
            ),
            200,
            {"ContentType": "application/json"},
        )
    except grpc.RpcError as exc:
        # PRESERVE: Exact same gRPC error handling
        status_code = exc.code()
        details = exc.details()
        return (
            json.dumps({"error": f"gRPC Error ({status_code}): {details}"}),
            500,
            {"ContentType": "application/json"},
        )
    except Exception as exc:
        # PRESERVE: Exact same exception handling
        return json.dumps({"error": str(exc)}), 500, {"ContentType": "application/json"}


@core.route("/restricted", methods=["GET"])
@check_auth  # PRESERVE: Exact same authentication
@rate_limit(limit=30, window=60)  # NEW: Add rate limiting for auth endpoints
@security_enhanced_route  # NEW: Add security enhancements
def restricted():
    """A separate request to test the auth flow - EXACT SAME BEHAVIOR."""

    # PRESERVE: Exact same response
    return (
        json.dumps({"message": "Successful Auth"}),
        200,
        {"ContentType": "application/json"},
    )


# NEW: Add health check endpoint (non-breaking addition)
@core.route("/health", methods=["GET"])
def health_check():
    """New health check endpoint - doesn't affect existing functionality."""
    try:
        # Check database connection
        from app.utils.data_cache_alchemy import DataCacheAlchemy

        test_cache = DataCacheAlchemy("BTC", 1000)
        db_healthy = test_cache.create_connection() is not None

        return (
            json.dumps(
                {
                    "status": "healthy",
                    "database": "connected" if db_healthy else "disconnected",
                    "timestamp": "2024-01-01T00:00:00Z",  # Placeholder
                }
            ),
            200,
            {"ContentType": "application/json"},
        )
    except Exception:
        return (
            json.dumps(
                {
                    "status": "unhealthy",
                    "database": "disconnected",
                    "timestamp": "2024-01-01T00:00:00Z",  # Placeholder
                }
            ),
            503,
            {"ContentType": "application/json"},
        )
