"""Unit tests for crypto service."""

from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

from app.domain.services import CryptoAnalysisService


class TestCryptoService:
    """Test crypto service functionality."""

    def test_analyze_investment_success(self):
        """Test successful investment analysis."""
        # Create mock repositories
        mock_price_repo = Mock()
        mock_investment_repo = Mock()

        # Configure mock price repo
        mock_price_repo.symbol_exists.return_value = True

        # Mock price data
        mock_price_data = Mock()
        mock_price_data.get_opening_average.return_value = Decimal("10000")
        mock_price_data.get_current_average.return_value = Decimal("15000")
        mock_price_data.to_chart_data.return_value = [{"x": "2023-01-01", "y": 10000}]
        mock_price_repo.get_price_data.return_value = mock_price_data

        # Create service with mocked repos
        service = CryptoAnalysisService(mock_price_repo, mock_investment_repo)

        # Test the service
        result = service.analyze_investment("BTC", Decimal(1000))

        # Verify the result
        assert "SYMBOL" in result
        assert "INVESTMENT" in result
        assert "PROFIT" in result
        assert "graph_data" in result
        assert result["SYMBOL"] == "BTC"
        assert result["INVESTMENT"] == 1000.0
        mock_investment_repo.log_query.assert_called_once()

    def test_analyze_investment_symbol_not_found(self):
        """Test investment analysis with non-existent symbol."""
        from app.domain.exceptions import SymbolNotFoundError

        # Create mock repositories
        mock_price_repo = Mock()
        mock_investment_repo = Mock()

        # Configure mock to return False for symbol_exists
        mock_price_repo.symbol_exists.return_value = False

        # Create service
        service = CryptoAnalysisService(mock_price_repo, mock_investment_repo)

        # Test that exception is raised
        with pytest.raises(SymbolNotFoundError):
            service.analyze_investment("INVALID", Decimal(1000))

    def test_analyze_investment_invalid_amount(self):
        """Test investment analysis with invalid amount."""
        from app.domain.exceptions import InvalidInvestmentError

        # Create mock repositories
        mock_price_repo = Mock()
        mock_investment_repo = Mock()

        # Create service
        service = CryptoAnalysisService(mock_price_repo, mock_investment_repo)

        # Test that exception is raised for negative amount
        with pytest.raises(InvalidInvestmentError):
            service.analyze_investment("BTC", Decimal(-1000))
