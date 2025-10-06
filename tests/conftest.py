"""Test configuration and fixtures."""

import pytest
import json
import os
from app import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def sample_crypto_data():
    """Sample crypto data for testing."""
    return {
        'symbol': 'BTC',
        'investment': 1000,
        'expected_fields': ['NUMBERCOINS', 'PROFIT', 'GROWTHFACTOR', 'LAMBOS', 'INVESTMENT', 'SYMBOL', 'GENERATIONDATE']
    }


@pytest.fixture
def sample_graph_data():
    """Sample graph data for testing."""
    return [
        {'x': '2023-01-01', 'y': 1000},
        {'x': '2023-01-02', 'y': 1050},
        {'x': '2023-01-03', 'y': 1100}
    ]


@pytest.fixture
def test_fixtures():
    """Load test fixtures from JSON file."""
    fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sample_data.json')
    with open(fixtures_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def mock_data_collector():
    """Mock data collector for testing."""
    from unittest.mock import Mock
    mock = Mock()
    mock.driver_logic.return_value = {
        'SYMBOL': 'BTC',
        'INVESTMENT': 1000,
        'NUMBERCOINS': 0.1,
        'PROFIT': 500,
        'GROWTHFACTOR': 1.5,
        'LAMBOS': 2.5,
        'GENERATIONDATE': '2023-01-01'
    }
    return mock


@pytest.fixture
def mock_graph_creator():
    """Mock graph creator for testing."""
    from unittest.mock import Mock
    mock = Mock()
    mock.driver_logic.return_value = [
        {'x': '2023-01-01', 'y': 1000},
        {'x': '2023-01-02', 'y': 1050}
    ]
    return mock
