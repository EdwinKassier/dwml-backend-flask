"""Integration tests for GraphQL endpoints."""

import json
from datetime import datetime, timezone

import pytest

from app import create_app


class TestGraphQLProcessRequest:
    """Test GraphQL process_request endpoint."""

    @pytest.fixture
    def app(self):
        """Create test application."""
        app = create_app("testing")
        return app

    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return app.test_client()

    def test_process_request_success(self, client, monkeypatch):
        """Test successful GraphQL process_request."""
        # Mock the crypto service
        mock_result = {
            "SYMBOL": "BTC",
            "INVESTMENT": 1000.0,
            "NUMBERCOINS": 0.05,
            "PROFIT": 250.0,
            "GROWTHFACTOR": 0.25,
            "LAMBOS": 0.00125,
            "GENERATIONDATE": datetime.now(timezone.utc).isoformat(),
            "graph_data": [{"x": "2023-01-01 00:00:00", "y": 20000.0}],
        }

        def mock_get_service():
            mock_service = type("MockService", (), {})()
            mock_service.analyze_investment = lambda symbol, amount: mock_result
            return mock_service

        monkeypatch.setattr(
            "app.domain.graphql_schema.get_crypto_service", mock_get_service
        )

        # GraphQL query
        query = """
        {
            processRequest(symbol: "BTC", investment: 1000) {
                message
                graphData
            }
        }
        """

        response = client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = response.get_json()

        # Verify GraphQL response structure
        assert "data" in data
        assert "processRequest" in data["data"]
        assert "message" in data["data"]["processRequest"]
        assert "graphData" in data["data"]["processRequest"]

        # Verify message content
        message = json.loads(data["data"]["processRequest"]["message"])
        assert message["SYMBOL"] == "BTC"
        assert message["INVESTMENT"] == 1000.0
        assert message["PROFIT"] == 250.0

        # Verify graph data
        graph_data = json.loads(data["data"]["processRequest"]["graphData"])
        assert len(graph_data) == 1
        assert graph_data[0]["y"] == 20000.0

    def test_process_request_empty_symbol(self, client):
        """Test GraphQL process_request with empty symbol."""
        query = """
        {
            processRequest(symbol: "", investment: 1000) {
                message
                graphData
            }
        }
        """

        response = client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = response.get_json()

        message = json.loads(data["data"]["processRequest"]["message"])
        assert "error" in message
        assert "Symbol parameter is required" in message["error"]

    def test_process_request_zero_investment(self, client):
        """Test GraphQL process_request with zero investment."""
        query = """
        {
            processRequest(symbol: "BTC", investment: 0) {
                message
                graphData
            }
        }
        """

        response = client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = response.get_json()

        message = json.loads(data["data"]["processRequest"]["message"])
        assert "error" in message
        assert "Investment must be greater than 0" in message["error"]

    def test_process_request_negative_investment(self, client):
        """Test GraphQL process_request with negative investment."""
        query = """
        {
            processRequest(symbol: "BTC", investment: -100) {
                message
                graphData
            }
        }
        """

        response = client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = response.get_json()

        message = json.loads(data["data"]["processRequest"]["message"])
        assert "error" in message
        assert "Investment must be greater than 0" in message["error"]

    def test_process_request_symbol_not_found(self, client, monkeypatch):
        """Test GraphQL process_request with non-existent symbol."""
        from app.domain.exceptions import SymbolNotFoundError

        def mock_get_service():
            mock_service = type("MockService", (), {})()

            def raise_not_found(symbol, amount):
                raise SymbolNotFoundError(f"Symbol {symbol} not found")

            mock_service.analyze_investment = raise_not_found
            return mock_service

        monkeypatch.setattr(
            "app.domain.graphql_schema.get_crypto_service", mock_get_service
        )

        query = """
        {
            processRequest(symbol: "INVALID", investment: 1000) {
                message
                graphData
            }
        }
        """

        response = client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = response.get_json()

        message = json.loads(data["data"]["processRequest"]["message"])
        assert "message" in message
        assert message["message"] == "Symbol doesn't exist"

    def test_process_request_invalid_investment_error(self, client, monkeypatch):
        """Test GraphQL process_request with InvalidInvestmentError."""
        from app.domain.exceptions import InvalidInvestmentError

        def mock_get_service():
            mock_service = type("MockService", (), {})()

            def raise_invalid(symbol, amount):
                raise InvalidInvestmentError("Investment amount is invalid")

            mock_service.analyze_investment = raise_invalid
            return mock_service

        monkeypatch.setattr(
            "app.domain.graphql_schema.get_crypto_service", mock_get_service
        )

        query = """
        {
            processRequest(symbol: "BTC", investment: 1000) {
                message
                graphData
            }
        }
        """

        response = client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = response.get_json()

        message = json.loads(data["data"]["processRequest"]["message"])
        assert "message" in message
        assert message["message"] == "Server Failure"
        assert "error" in message

    def test_process_request_insufficient_data_error(self, client, monkeypatch):
        """Test GraphQL process_request with InsufficientPriceDataError."""
        from app.domain.exceptions import InsufficientPriceDataError

        def mock_get_service():
            mock_service = type("MockService", (), {})()

            def raise_insufficient(symbol, amount):
                raise InsufficientPriceDataError("Not enough price data")

            mock_service.analyze_investment = raise_insufficient
            return mock_service

        monkeypatch.setattr(
            "app.domain.graphql_schema.get_crypto_service", mock_get_service
        )

        query = """
        {
            processRequest(symbol: "BTC", investment: 1000) {
                message
                graphData
            }
        }
        """

        response = client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = response.get_json()

        message = json.loads(data["data"]["processRequest"]["message"])
        assert "message" in message
        assert message["message"] == "Server Failure"
        assert "error" in message

    def test_process_request_external_service_error(self, client, monkeypatch):
        """Test GraphQL process_request with ExternalServiceError."""
        from app.domain.exceptions import ExternalServiceError

        def mock_get_service():
            mock_service = type("MockService", (), {})()

            def raise_external(symbol, amount):
                raise ExternalServiceError("External API failed")

            mock_service.analyze_investment = raise_external
            return mock_service

        monkeypatch.setattr(
            "app.domain.graphql_schema.get_crypto_service", mock_get_service
        )

        query = """
        {
            processRequest(symbol: "BTC", investment: 1000) {
                message
                graphData
            }
        }
        """

        response = client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = response.get_json()

        message = json.loads(data["data"]["processRequest"]["message"])
        assert "message" in message
        assert message["message"] == "Server Failure"

    def test_process_request_unexpected_error(self, client, monkeypatch):
        """Test GraphQL process_request with unexpected exception."""

        def mock_get_service():
            mock_service = type("MockService", (), {})()

            def raise_unexpected(symbol, amount):
                raise RuntimeError("Unexpected error occurred")

            mock_service.analyze_investment = raise_unexpected
            return mock_service

        monkeypatch.setattr(
            "app.domain.graphql_schema.get_crypto_service", mock_get_service
        )

        query = """
        {
            processRequest(symbol: "BTC", investment: 1000) {
                message
                graphData
            }
        }
        """

        response = client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = response.get_json()

        message = json.loads(data["data"]["processRequest"]["message"])
        assert "message" in message
        assert message["message"] == "Server Failure"

    def test_process_request_whitespace_symbol(self, client, monkeypatch):
        """Test GraphQL process_request with whitespace-only symbol."""
        query = """
        {
            processRequest(symbol: "   ", investment: 1000) {
                message
                graphData
            }
        }
        """

        response = client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = response.get_json()

        message = json.loads(data["data"]["processRequest"]["message"])
        assert "error" in message
        assert "Symbol parameter is required" in message["error"]

    def test_process_request_symbol_with_spaces(self, client, monkeypatch):
        """Test GraphQL process_request strips whitespace from symbol."""
        mock_result = {
            "SYMBOL": "BTC",
            "INVESTMENT": 1000.0,
            "NUMBERCOINS": 0.05,
            "PROFIT": 250.0,
            "GROWTHFACTOR": 0.25,
            "LAMBOS": 0.00125,
            "GENERATIONDATE": datetime.now(timezone.utc).isoformat(),
            "graph_data": [],
        }

        def mock_get_service():
            mock_service = type("MockService", (), {})()
            mock_service.analyze_investment = lambda symbol, amount: mock_result
            return mock_service

        monkeypatch.setattr(
            "app.domain.graphql_schema.get_crypto_service", mock_get_service
        )

        query = """
        {
            processRequest(symbol: "  BTC  ", investment: 1000) {
                message
                graphData
            }
        }
        """

        response = client.post(
            "/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = response.get_json()

        message = json.loads(data["data"]["processRequest"]["message"])
        assert message["SYMBOL"] == "BTC"
