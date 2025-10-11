"""Unit tests for validation schemas."""

import pytest
from marshmallow import ValidationError

from app.domain.schemas import (
    CryptoAnalysisRequestSchema,
    CryptoAnalysisResponseSchema,
    ErrorResponseSchema,
    HealthCheckSchema,
    validate_crypto_request,
    validate_health_response,
)


class TestCryptoAnalysisRequestSchema:
    """Test crypto analysis request schema."""

    def test_valid_request(self):
        """Test valid request data."""
        schema = CryptoAnalysisRequestSchema()
        data = {"symbol": "BTC", "investment": 1000}

        result = schema.load(data)
        assert result["symbol"] == "BTC"
        assert result["investment"] == 1000

    def test_invalid_symbol(self):
        """Test invalid symbol format."""
        schema = CryptoAnalysisRequestSchema()
        data = {"symbol": "btc", "investment": 1000}  # lowercase

        with pytest.raises(ValidationError):
            schema.load(data)

    def test_invalid_investment(self):
        """Test invalid investment amount."""
        schema = CryptoAnalysisRequestSchema()
        data = {"symbol": "BTC", "investment": -100}  # negative

        with pytest.raises(ValidationError):
            schema.load(data)

    def test_missing_fields(self):
        """Test missing required fields."""
        schema = CryptoAnalysisRequestSchema()
        data = {"symbol": "BTC"}  # missing investment

        with pytest.raises(ValidationError):
            schema.load(data)


class TestCryptoAnalysisResponseSchema:
    """Test crypto analysis response schema."""

    def test_valid_response(self):
        """Test valid response data."""
        schema = CryptoAnalysisResponseSchema()
        data = {
            "message": {"profit": 1000},
            "graph_data": [{"x": "2023-01-01", "y": 1000}],
            "success": True,
        }

        result = schema.load(data)
        assert result["message"] == {"profit": 1000}
        assert result["graph_data"] == [{"x": "2023-01-01", "y": 1000}]
        assert result["success"] is True


class TestHealthCheckSchema:
    """Test health check schema."""

    def test_valid_health_check(self):
        """Test valid health check data."""
        schema = HealthCheckSchema()
        data = {"status": "healthy", "service": "dwml-backend", "version": "1.0.0"}

        result = schema.load(data)
        assert result["status"] == "healthy"
        assert result["service"] == "dwml-backend"
        assert result["version"] == "1.0.0"


class TestErrorResponseSchema:
    """Test error response schema."""

    def test_valid_error_response(self):
        """Test valid error response data."""
        schema = ErrorResponseSchema()
        data = {
            "error": "Validation Error",
            "message": "Invalid input",
            "status_code": 400,
        }

        result = schema.load(data)
        assert result["error"] == "Validation Error"
        assert result["message"] == "Invalid input"
        assert result["status_code"] == 400


class TestValidationFunctions:
    """Test validation helper functions."""

    def test_validate_crypto_request_valid(self):
        """Test valid crypto request validation."""
        data = {"symbol": "BTC", "investment": 1000}
        is_valid, errors = validate_crypto_request(data)

        assert is_valid is True
        assert errors == {}

    def test_validate_crypto_request_invalid(self):
        """Test invalid crypto request validation."""
        data = {"symbol": "btc", "investment": -100}
        is_valid, errors = validate_crypto_request(data)

        assert is_valid is False
        assert "symbol" in errors
        assert "investment" in errors

    def test_validate_health_response_valid(self):
        """Test valid health response validation."""
        data = {"status": "healthy", "service": "dwml-backend", "version": "1.0.0"}
        is_valid, errors = validate_health_response(data)

        assert is_valid is True
        assert errors == {}

    def test_validate_health_response_invalid(self):
        """Test invalid health response validation."""
        data = {"status": "healthy"}  # missing required fields
        is_valid, errors = validate_health_response(data)

        assert is_valid is False
        assert "service" in errors
        assert "version" in errors
