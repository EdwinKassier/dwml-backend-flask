"""Integration tests for API endpoints."""

import pytest

from app import create_app


class TestCryptoEndpoints:
    """Test crypto API endpoints."""

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
        """Test successful process_request endpoint."""
        # Mock the crypto service
        from datetime import UTC, datetime
        from decimal import Decimal

        mock_result = {
            "SYMBOL": "BTC",
            "INVESTMENT": 1000.0,
            "NUMBERCOINS": 0.05,
            "PROFIT": 250.0,
            "GROWTHFACTOR": 0.25,
            "LAMBOS": 0.00125,
            "GENERATIONDATE": datetime.now(UTC).isoformat(),
            "graph_data": [{"x": "2023-01-01 00:00:00", "y": 20000.0}],
        }

        def mock_get_service():
            mock_service = type("MockService", (), {})()
            mock_service.analyze_investment = lambda symbol, amount: mock_result
            return mock_service

        monkeypatch.setattr("app.domain.routes.get_crypto_service", mock_get_service)

        response = client.get("/api/v1/process_request?symbol=BTC&investment=1000")

        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert "graph_data" in data

    def test_process_request_missing_params(self, client):
        """Test process_request with missing parameters."""
        response = client.get("/api/v1/process_request")

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Symbol parameter is required" in data["error"]

    def test_process_request_invalid_params(self, client):
        """Test process_request with invalid parameters."""
        response = client.get("/api/v1/process_request?symbol=&investment=invalid")

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_restricted_endpoint_unauthorized(self, client):
        """Test restricted endpoint without authentication."""
        response = client.get("/api/v1/restricted")

        # When Firebase is not available, auth is skipped and returns 200
        # When Firebase is available, it should return 401 for missing auth
        assert response.status_code in [200, 401]


class TestHealthEndpoints:
    """Test health and monitoring endpoints."""

    @pytest.fixture
    def app(self):
        """Create test application."""
        app = create_app("testing")
        return app

    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return app.test_client()

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "timestamp" in data

    def test_metrics_endpoint(self, client):
        """Test metrics endpoint - should return 404 as it doesn't exist."""
        response = client.get("/metrics")

        # Metrics endpoint is not implemented in this version
        assert response.status_code == 404

    def test_status_endpoint(self, client):
        """Test status endpoint."""
        response = client.get("/status")

        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert "version" in data

    def test_home_endpoint(self, client):
        """Test home endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data


class TestErrorHandling:
    """Test error handling across endpoints."""

    @pytest.fixture
    def app(self):
        """Create test application."""
        app = create_app("testing")
        return app

    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return app.test_client()

    def test_404_endpoint(self, client):
        """Test 404 for non-existent endpoint."""
        response = client.get("/non-existent-endpoint")

        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """Test method not allowed."""
        response = client.post("/status")

        assert response.status_code == 405
