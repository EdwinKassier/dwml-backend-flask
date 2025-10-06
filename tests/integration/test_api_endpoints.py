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

    def test_process_request_success(self, client):
        """Test successful process_request endpoint."""
        with pytest.MonkeyPatch().context() as m:
            # Mock the data collector and graph creator
            m.setattr(
                "app.utils.data_collector.DataCollector.driver_logic",
                lambda self: {"profit": 1000},
            )
            m.setattr(
                "app.utils.graph_creator.GraphCreator.driver_logic",
                lambda self: [{"x": "2023-01-01", "y": 1000}],
            )

            response = client.get(
                "/api/v1/project/core/process_request?symbol=BTC&investment=1000"
            )

            assert response.status_code == 200
            data = response.get_json()
            assert "message" in data
            assert "graph_data" in data

    def test_process_request_missing_params(self, client):
        """Test process_request with missing parameters."""
        response = client.get("/api/v1/project/core/process_request")

        assert response.status_code == 500
        data = response.get_json()
        assert data["message"] == "Server Failure"

    def test_process_request_invalid_params(self, client):
        """Test process_request with invalid parameters."""
        response = client.get(
            "/api/v1/project/core/process_request?symbol=&investment=invalid"
        )

        assert response.status_code == 500
        data = response.get_json()
        assert data["message"] == "Server Failure"

    def test_restricted_endpoint_unauthorized(self, client):
        """Test restricted endpoint without authentication."""
        response = client.get("/api/v1/project/core/restricted")

        assert response.status_code == 401


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
        assert "version" in data

    def test_metrics_endpoint(self, client):
        """Test metrics endpoint."""
        response = client.get("/metrics")

        assert response.status_code == 200
        data = response.get_json()
        assert "uptime" in data
        assert "status" in data
        assert "version" in data

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
