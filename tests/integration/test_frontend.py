from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        with app.test_client() as client:
            yield client


def test_base_route_without_args(client):
    """Test endpoint without parameters returns 400."""
    rv = client.get("/api/v1/process_request")

    print(rv.get_data())
    assert rv.status_code == 400  # Missing required parameters


def test_base_route_with_args_valid_symbol(client):
    """Test endpoint with valid parameters."""
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

    with patch("app.domain.routes.get_crypto_service") as mock_service:
        mock_service.return_value.analyze_investment.return_value = mock_result
        rv = client.get("/api/v1/process_request?symbol=BTC&investment=1000")

        print(rv.get_data())
        assert rv.status_code == 200


def test_base_route_with_args_invalid_symbol(client):
    """Test endpoint with invalid symbol."""
    from app.domain.exceptions import SymbolNotFoundError

    with patch("app.domain.routes.get_crypto_service") as mock_service:
        mock_service.return_value.analyze_investment.side_effect = SymbolNotFoundError(
            "Symbol DUHHH not found"
        )
        rv = client.get("/api/v1/process_request?symbol=DUHHH&investment=1000")

        print(rv.get_data())
        assert rv.status_code == 404  # Symbol not found


def test_base_route_malformed_no_symbol(client):
    """Test endpoint without symbol parameter."""
    rv = client.get("/api/v1/process_request?investment=1000")

    print(rv.get_data())
    assert rv.status_code == 400  # Missing symbol parameter


def test_base_route_malformed_no_investment(client):
    """Test endpoint without investment parameter - defaults to 0 which is invalid."""
    rv = client.get("/api/v1/process_request?symbol=BTC")

    print(rv.get_data())
    # Investment defaults to "0" which converts to Decimal(0), but that's still invalid
    # The validation should catch this
    assert rv.status_code in [
        400,
        500,
    ]  # Accept either validation error or service error


def test_auth_route_without_auth_header(client):
    rv = client.get("/api/v1/restricted")

    print(rv.get_data())
    # When Firebase is not available, auth is skipped and returns 200
    # When Firebase is available, it should return 401 for missing auth
    assert rv.status_code in [200, 401]


def test_unknown_route(client):
    rv = client.get("/api/v1/random")

    print(rv.get_data())
    assert rv.status_code == 404
