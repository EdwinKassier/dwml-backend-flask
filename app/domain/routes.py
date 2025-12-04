"""Domain routes for DWML process_request endpoints."""

import json
from decimal import Decimal
from typing import Tuple

import grpc
from flask import Blueprint, current_app, request

from app.domain.exceptions import (
    ExternalServiceError,
    InsufficientPriceDataError,
    InvalidInvestmentError,
    SymbolNotFoundError,
)
from app.domain.proto_files import api_pb2 as pb2
from app.domain.proto_files import api_pb2_grpc as pb2_grpc
from app.domain.services import CryptoAnalysisService
from app.shared.middleware.auth import check_auth
from app.shared.middleware.rate_limit import rate_limit
from app.shared.middleware.security import security_enhanced_route

# Create blueprint for crypto domain
crypto_bp = Blueprint("crypto", __name__)


def get_crypto_service() -> CryptoAnalysisService:
    """
    Get crypto service instance with wired infrastructure.
    """
    from app.domain import investment_repo, price_repo

    return CryptoAnalysisService(price_repo, investment_repo)


@crypto_bp.before_request
def before_request_func() -> None:
    """Ensure logger name is set."""
    current_app.logger.name = "crypto"


@crypto_bp.route("/process_request", methods=["GET"])
@rate_limit(limit=60, window=60)
@security_enhanced_route
def analyze_investment() -> Tuple[str, int, dict[str, str]]:
    """
    Analyze crypto investment.

    GET /api/v1/process_request?symbol=BTC&investment=1000

    Returns:
        JSON with analysis results and graph data
    """
    current_app.logger.info("Investment analysis request received")

    try:
        # 1. Parse request parameters
        symbol = request.args.get("symbol", "").strip()
        investment_str = request.args.get("investment", "0")

        # 2. Basic validation
        if not symbol:
            return (
                json.dumps({"error": "Symbol parameter is required"}),
                400,
                {"Content-Type": "application/json"},
            )

        try:
            investment = Decimal(investment_str)
        except (ValueError, TypeError):
            return (
                json.dumps({"error": "Investment must be a valid number"}),
                400,
                {"Content-Type": "application/json"},
            )

        # 3. Execute business logic via service
        service = get_crypto_service()
        result = service.analyze_investment(symbol, investment)

        # 4. Return successful response in expected format
        graph_data = result.pop("graph_data", [])
        return (
            json.dumps({"message": result, "graph_data": graph_data}),
            200,
            {"Content-Type": "application/json"},
        )

    except InvalidInvestmentError as e:
        current_app.logger.warning(f"Invalid investment: {e}")
        return (
            json.dumps({"message": "Server Failure", "error": str(e)}),
            400,
            {"Content-Type": "application/json"},
        )

    except SymbolNotFoundError as e:
        current_app.logger.warning(f"Symbol not found: {e}")
        return (
            json.dumps({"message": "Symbol doesn't exist"}),
            404,
            {"Content-Type": "application/json"},
        )

    except InsufficientPriceDataError as e:
        current_app.logger.error(f"Insufficient data: {e}")
        return (
            json.dumps({"message": "Server Failure", "error": str(e)}),
            503,
            {"Content-Type": "application/json"},
        )

    except ExternalServiceError as e:
        current_app.logger.error(f"External service error: {e}")
        return (
            json.dumps({"message": "Server Failure"}),
            503,
            {"Content-Type": "application/json"},
        )

    except Exception as e:
        current_app.logger.error(f"Unexpected error: {e}", exc_info=True)
        return (
            json.dumps({"message": "Server Failure"}),
            500,
            {"Content-Type": "application/json"},
        )


@crypto_bp.route("/process_request_grpc", methods=["GET"])
@rate_limit(limit=60, window=60)
@security_enhanced_route
def analyze_investment_grpc() -> Tuple[str, int, dict[str, str]]:
    """
    Analyze crypto investment via gRPC.

    GET /api/v1/process_request_grpc?symbol=BTC&investment=1000

    Returns:
        JSON with analysis results from gRPC service
    """
    current_app.logger.info("gRPC investment analysis request received")

    try:
        # Parse parameters
        symbol = str(request.args.get("symbol", "").strip())
        investment = int(request.args.get("investment", 0))

        current_app.logger.info(f"gRPC request for {symbol}:{investment}")

        # Basic validation
        if not symbol or investment <= 0:
            return (
                json.dumps({"error": "Invalid parameters"}),
                400,
                {"ContentType": "application/json"},
            )

        # Call gRPC service
        endpoint = "master-dwml-backend-python-grpc-lqfbwlkw2a-uc.a.run.app"
        channel = grpc.secure_channel(endpoint, grpc.ssl_channel_credentials())
        stub = pb2_grpc.APIStub(channel)

        current_app.logger.info(f"Calling gRPC stub: {stub}")
        response = stub.processRequest(
            pb2.apiRequest(symbol=symbol, investment=investment)
        )
        current_app.logger.info(f"gRPC response received: {response}")

        # Return response
        return (
            json.dumps(
                {"message": response.message, "graph_data": response.graph_data}
            ),
            200,
            {"ContentType": "application/json"},
        )

    except grpc.RpcError as exc:
        status_code = exc.code()
        details = exc.details()
        current_app.logger.error(f"gRPC Error ({status_code}): {details}")
        return (
            json.dumps({"error": f"gRPC Error ({status_code}): {details}"}),
            500,
            {"ContentType": "application/json"},
        )

    except Exception as exc:
        current_app.logger.error(f"Unexpected error in gRPC call: {exc}", exc_info=True)
        return (
            json.dumps({"error": str(exc)}),
            500,
            {"ContentType": "application/json"},
        )


@crypto_bp.route("/restricted", methods=["GET"])
@check_auth
@rate_limit(limit=30, window=60)
@security_enhanced_route
def restricted() -> Tuple[str, int, dict[str, str]]:
    """
    Authenticated endpoint for testing.

    Requires valid Firebase auth token.
    """
    return (
        json.dumps({"message": "Successful Auth"}),
        200,
        {"ContentType": "application/json"},
    )


@crypto_bp.route("/analyze_async", methods=["POST"])
@rate_limit(limit=30, window=60)
@security_enhanced_route
def analyze_investment_async() -> Tuple[str, int, dict[str, str]]:
    """
    Submit crypto investment analysis as background task.

    POST /api/v1/analyze_async
    Body: {"symbol": "BTC", "investment": 1000, "user_id": "optional"}

    Returns:
        JSON with task ID for status checking
    """
    current_app.logger.info("Async investment analysis request received")

    try:
        # Check if Celery is available
        if not hasattr(current_app, "celery") or current_app.celery is None:
            return (
                json.dumps(
                    {
                        "error": "Background tasks not available",
                        "message": "Celery is not configured. Use /process_request for synchronous analysis.",
                    }
                ),
                503,
                {"Content-Type": "application/json"},
            )

        data = request.get_json()
        if not data:
            return (
                json.dumps({"error": "Request body is required"}),
                400,
                {"Content-Type": "application/json"},
            )

        symbol = data.get("symbol", "").strip()
        investment = data.get("investment", 0)
        user_id = data.get("user_id")

        if not symbol or investment <= 0:
            return (
                json.dumps({"error": "Valid symbol and investment required"}),
                400,
                {"Content-Type": "application/json"},
            )

        # Import and submit task
        from app.domain.tasks import analyze_investment_async as analyze_task

        task = analyze_task.delay(
            symbol=symbol, amount=float(investment), user_id=user_id
        )

        return (
            json.dumps(
                {
                    "message": "Analysis submitted successfully",
                    "task_id": task.id,
                    "status_url": f"/api/v1/task_status/{task.id}",
                    "symbol": symbol,
                    "amount": investment,
                }
            ),
            202,
            {"Content-Type": "application/json"},
        )

    except Exception as e:
        current_app.logger.error(f"Error submitting async task: {e}", exc_info=True)
        return (
            json.dumps({"error": "Failed to submit task", "details": str(e)}),
            500,
            {"Content-Type": "application/json"},
        )


@crypto_bp.route("/task_status/<task_id>", methods=["GET"])
@rate_limit(limit=60, window=60)
def check_task_status(task_id: str) -> Tuple[str, int, dict[str, str]]:
    """
    Check status of background task.

    GET /api/v1/task_status/<task_id>

    Returns:
        JSON with task status and result if completed
    """
    try:
        if not hasattr(current_app, "celery") or current_app.celery is None:
            return (
                json.dumps({"error": "Background tasks not available"}),
                503,
                {"Content-Type": "application/json"},
            )

        from celery.result import AsyncResult

        task = AsyncResult(task_id, app=current_app.celery)

        response = {
            "task_id": task_id,
            "status": task.state,
        }

        if task.state == "PENDING":
            response["message"] = "Task is waiting to be processed"
        elif task.state == "STARTED":
            response["message"] = "Task is being processed"
        elif task.state == "PROGRESS":
            response["message"] = "Task is in progress"
            response["progress"] = task.info if task.info else {}
        elif task.state == "SUCCESS":
            response["message"] = "Task completed successfully"
            response["result"] = task.result
        elif task.state == "FAILURE":
            response["message"] = "Task failed"
            response["error"] = str(task.info)
        elif task.state == "RETRY":
            response["message"] = "Task is being retried"
            response["retry_count"] = task.info.get("retry_count") if task.info else 0
        else:
            response["message"] = f"Task state: {task.state}"

        return (
            json.dumps(response),
            200,
            {"Content-Type": "application/json"},
        )

    except Exception as e:
        current_app.logger.error(f"Error checking task status: {e}", exc_info=True)
        return (
            json.dumps({"error": "Failed to check task status", "details": str(e)}),
            500,
            {"Content-Type": "application/json"},
        )
