"""Unit tests for domain models."""

from datetime import datetime
from decimal import Decimal

import pytest

from app.domain.exceptions import InsufficientPriceDataError, InvalidInvestmentError
from app.domain.models import Investment, PriceData


class TestInvestment:
    """Test Investment domain model."""

    def test_investment_creation(self):
        """Test creating a valid investment."""
        investment = Investment(symbol="BTC", amount=Decimal(1000))

        assert investment.symbol == "BTC"
        assert investment.amount == Decimal(1000)
        assert isinstance(investment.created_at, datetime)

    def test_investment_symbol_normalization(self):
        """Test that symbol is normalized to uppercase."""
        investment = Investment(symbol="btc", amount=Decimal(1000))

        assert investment.symbol == "BTC"

    def test_investment_invalid_amount(self):
        """Test that negative amount raises error."""
        with pytest.raises(InvalidInvestmentError):
            Investment(symbol="BTC", amount=Decimal(-100))

    def test_investment_zero_amount(self):
        """Test that zero amount raises error."""
        with pytest.raises(InvalidInvestmentError):
            Investment(symbol="BTC", amount=Decimal(0))

    def test_investment_invalid_symbol(self):
        """Test that invalid symbol raises error."""
        with pytest.raises(InvalidInvestmentError):
            Investment(symbol="", amount=Decimal(1000))

    def test_investment_symbol_too_long(self):
        """Test that too long symbol raises error."""
        with pytest.raises(InvalidInvestmentError):
            Investment(symbol="VERYLONGSYMBOL", amount=Decimal(1000))

    def test_calculate_coins_purchased(self):
        """Test calculating number of coins purchased."""
        investment = Investment(symbol="BTC", amount=Decimal(1000))
        coins = investment.calculate_coins_purchased(Decimal(10000))

        assert coins == Decimal("0.1")

    def test_calculate_profit(self):
        """Test calculating profit."""
        investment = Investment(symbol="BTC", amount=Decimal(1000))
        profit = investment.calculate_profit(Decimal(10000), Decimal(15000))

        # 1000 / 10000 = 0.1 coins
        # 0.1 * 15000 = 1500 current value
        # 1500 - 1000 = 500 profit
        assert profit == Decimal(500)

    def test_calculate_growth_factor(self):
        """Test calculating growth factor."""
        investment = Investment(symbol="BTC", amount=Decimal(1000))
        growth = investment.calculate_growth_factor(Decimal(10000), Decimal(15000))

        # Profit is 500, investment is 1000
        # Growth factor = 500 / 1000 = 0.5
        assert growth == Decimal("0.5")

    def test_calculate_lambos(self):
        """Test calculating Lamborghini equivalent."""
        investment = Investment(symbol="BTC", amount=Decimal(1000))
        lambos = investment.calculate_lambos(Decimal(10000), Decimal(15000))

        # Profit is 500, Lambo price is 200000
        # Lambos = 500 / 200000 = 0.0025
        assert lambos == Decimal("0.0025")


class TestPriceData:
    """Test PriceData domain model."""

    def test_price_data_creation(self):
        """Test creating price data."""
        prices = [
            (datetime(2023, 1, 1), Decimal(10000)),
            (datetime(2023, 1, 2), Decimal(11000)),
            (datetime(2023, 1, 3), Decimal(12000)),
            (datetime(2023, 1, 4), Decimal(13000)),
        ]

        price_data = PriceData(symbol="BTC", prices=prices)

        assert price_data.symbol == "BTC"
        assert len(price_data.prices) == 4

    def test_price_data_empty_raises_error(self):
        """Test that empty price list raises error."""
        with pytest.raises(InsufficientPriceDataError):
            PriceData(symbol="BTC", prices=[])

    def test_get_opening_average(self):
        """Test getting opening average."""
        prices = [
            (datetime(2023, 1, 1), Decimal(10000)),
            (datetime(2023, 1, 2), Decimal(12000)),
            (datetime(2023, 1, 3), Decimal(14000)),
            (datetime(2023, 1, 4), Decimal(16000)),
            (datetime(2023, 1, 5), Decimal(18000)),
        ]

        price_data = PriceData(symbol="BTC", prices=prices)
        opening_avg = price_data.get_opening_average(weeks=4)

        # Average of first 4: (10000 + 12000 + 14000 + 16000) / 4 = 13000
        assert opening_avg == Decimal(13000)

    def test_get_current_average(self):
        """Test getting current average."""
        prices = [
            (datetime(2023, 1, 1), Decimal(10000)),
            (datetime(2023, 1, 2), Decimal(12000)),
            (datetime(2023, 1, 3), Decimal(14000)),
            (datetime(2023, 1, 4), Decimal(16000)),
            (datetime(2023, 1, 5), Decimal(18000)),
        ]

        price_data = PriceData(symbol="BTC", prices=prices)
        current_avg = price_data.get_current_average(weeks=4)

        # Average of last 4: (12000 + 14000 + 16000 + 18000) / 4 = 15000
        assert current_avg == Decimal(15000)

    def test_insufficient_data_for_opening_average(self):
        """Test that insufficient data raises error."""
        prices = [
            (datetime(2023, 1, 1), Decimal(10000)),
            (datetime(2023, 1, 2), Decimal(12000)),
        ]

        price_data = PriceData(symbol="BTC", prices=prices)

        with pytest.raises(InsufficientPriceDataError):
            price_data.get_opening_average(weeks=4)

    def test_to_chart_data(self):
        """Test converting to chart format."""
        prices = [
            (datetime(2023, 1, 1, 12, 0, 0), Decimal(10000)),
            (datetime(2023, 1, 2, 12, 0, 0), Decimal(11000)),
        ]

        price_data = PriceData(symbol="BTC", prices=prices)
        chart_data = price_data.to_chart_data()

        assert len(chart_data) == 2
        assert chart_data[0]["x"] == "2023-01-01 12:00:00"
        assert chart_data[0]["y"] == 10000.0
        assert chart_data[1]["x"] == "2023-01-02 12:00:00"
        assert chart_data[1]["y"] == 11000.0
