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
    Get crypto service instance.

    NOTE: This needs to be wired up to your external infrastructure.
    Import your repositories here and create the service:

    Example:
        from your_infrastructure import PriceRepository, InvestmentRepository
        price_repo = PriceRepository(current_app.config['KRAKEN_API_URL'])
        investment_repo = InvestmentRepository()
        return CryptoAnalysisService(price_repo, investment_repo)
    """
    # TODO: Wire up to external infrastructure
    raise NotImplementedError(
        "Connect to your external infrastructure here. "
        "Import repositories and create CryptoAnalysisService."
    )


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
