import json
from decimal import Decimal

import strawberry
from flask import current_app

from app.domain.exceptions import CryptoDomainError


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

        NOTE: Wire this up to your external infrastructure.
        Import your service factory or create service here.
        """
        try:
            # TODO: Connect to external infrastructure
            # from your_infrastructure import get_crypto_service
            # service = get_crypto_service()
            # result = service.analyze_investment(symbol, Decimal(investment))

            raise NotImplementedError(
                "GraphQL endpoint needs to be wired to external infrastructure"
            )

        except CryptoDomainError as exc:
            current_app.logger.warning(f"Domain error in GraphQL: {exc}")
            return ProcessRequestResult(
                message=json.dumps({"error": str(exc)}), graph_data="[]"
            )
        except Exception as exc:
            current_app.logger.error(f"Unexpected error in GraphQL: {exc}")
            return ProcessRequestResult(
                message=json.dumps({"error": "Symbol doesn't exist"}), graph_data="[]"
            )


schema = strawberry.Schema(query=Query)
