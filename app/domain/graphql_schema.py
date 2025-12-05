import json
from decimal import Decimal

import strawberry
from flask import current_app

from app.domain.exceptions import (
    ExternalServiceError,
    InsufficientPriceDataError,
    InvalidInvestmentError,
    SymbolNotFoundError,
)
from app.domain.routes import get_crypto_service


@strawberry.type
class ProcessRequestResult:
    message: str
    graph_data: str


# Define a GraphQL schema
@strawberry.type
class Query:
    @strawberry.field
    def process_request(self, symbol: str, investment: int) -> ProcessRequestResult:
        """
        Process crypto investment request via GraphQL.

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC')
            investment: Investment amount in USD

        Returns:
            ProcessRequestResult with analysis data and graph data
        """
        current_app.logger.info(
            f"GraphQL investment analysis request: {symbol}, {investment}"
        )

        try:
            # Validate parameters
            if not symbol or not symbol.strip():
                return ProcessRequestResult(
                    message=json.dumps({"error": "Symbol parameter is required"}),
                    graph_data="[]",
                )

            if investment <= 0:
                return ProcessRequestResult(
                    message=json.dumps({"error": "Investment must be greater than 0"}),
                    graph_data="[]",
                )

            # Get service instance with wired infrastructure
            service = get_crypto_service()

            # Execute business logic
            result = service.analyze_investment(symbol.strip(), Decimal(investment))

            # Extract graph data and format response
            graph_data = result.pop("graph_data", [])

            return ProcessRequestResult(
                message=json.dumps(result), graph_data=json.dumps(graph_data)
            )

        except InvalidInvestmentError as exc:
            current_app.logger.warning(f"Invalid investment in GraphQL: {exc}")
            return ProcessRequestResult(
                message=json.dumps({"message": "Server Failure", "error": str(exc)}),
                graph_data="[]",
            )

        except SymbolNotFoundError as exc:
            current_app.logger.warning(f"Symbol not found in GraphQL: {exc}")
            return ProcessRequestResult(
                message=json.dumps({"message": "Symbol doesn't exist"}),
                graph_data="[]",
            )

        except InsufficientPriceDataError as exc:
            current_app.logger.error(f"Insufficient data in GraphQL: {exc}")
            return ProcessRequestResult(
                message=json.dumps({"message": "Server Failure", "error": str(exc)}),
                graph_data="[]",
            )

        except ExternalServiceError as exc:
            current_app.logger.error(f"External service error in GraphQL: {exc}")
            return ProcessRequestResult(
                message=json.dumps({"message": "Server Failure"}), graph_data="[]"
            )

        except Exception as exc:
            current_app.logger.error(
                f"Unexpected error in GraphQL: {exc}", exc_info=True
            )
            return ProcessRequestResult(
                message=json.dumps({"message": "Server Failure"}), graph_data="[]"
            )


schema = strawberry.Schema(query=Query)
