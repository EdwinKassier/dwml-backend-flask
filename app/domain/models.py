"""Domain models with business logic."""
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal

from .constants import (
    CURRENT_PERIOD_WEEKS,
    DATE_TIME_FORMAT,
    LAMBO_PRICE,
    OPENING_PERIOD_WEEKS,
)
from .exceptions import InsufficientPriceDataError, InvalidInvestmentError


@dataclass
class Investment:
    """
    Investment domain model with validation and business logic.

    Represents a cryptocurrency investment with amount and symbol.
    Contains business rules for validation and profit calculations.
    """

    symbol: str
    amount: Decimal
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Validate investment data on creation."""
        # Normalize symbol
        self.symbol = self.symbol.upper().strip()

        # Validate symbol
        if not self.symbol or len(self.symbol) > 10:
            raise InvalidInvestmentError(f"Invalid symbol: {self.symbol}")

        # Validate amount
        if self.amount <= 0:
            raise InvalidInvestmentError("Investment amount must be positive")

        # Ensure Decimal type
        if not isinstance(self.amount, Decimal):
            self.amount = Decimal(str(self.amount))

    def calculate_coins_purchased(self, opening_price: Decimal) -> Decimal:
        """
        Calculate number of coins purchased at opening price.

        Args:
            opening_price: Opening price per coin

        Returns:
            Number of coins that can be purchased

        Raises:
            InvalidInvestmentError: If opening price is invalid
        """
        if opening_price <= 0:
            raise InvalidInvestmentError("Opening price must be positive")
        return self.amount / opening_price

    def calculate_profit(
        self, opening_price: Decimal, current_price: Decimal
    ) -> Decimal:
        """
        Calculate profit from investment.

        Args:
            opening_price: Price when investment was made
            current_price: Current price

        Returns:
            Profit amount (can be negative for loss)
        """
        coins = self.calculate_coins_purchased(opening_price)
        current_value = coins * current_price
        return current_value - self.amount

    def calculate_growth_factor(
        self, opening_price: Decimal, current_price: Decimal
    ) -> Decimal:
        """
        Calculate growth factor as a ratio.

        Args:
            opening_price: Initial price
            current_price: Current price

        Returns:
            Growth factor (profit / investment)
        """
        profit = self.calculate_profit(opening_price, current_price)
        return profit / self.amount

    def calculate_lambos(
        self, opening_price: Decimal, current_price: Decimal
    ) -> Decimal:
        """
        Calculate Lamborghini equivalent of profit.

        Args:
            opening_price: Initial price
            current_price: Current price

        Returns:
            Number of Lamborghinis that could be purchased with profit
        """
        profit = self.calculate_profit(opening_price, current_price)
        return profit / LAMBO_PRICE


@dataclass
class PriceData:
    """
    Price data domain model with analysis methods.

    Represents historical price data for a cryptocurrency
    with methods to calculate averages and export for charts.
    """

    symbol: str
    prices: list[tuple[datetime, Decimal]]

    def __post_init__(self) -> None:
        """Validate price data on creation."""
        if not self.prices:
            raise InsufficientPriceDataError(
                f"No price data available for {self.symbol}"
            )

    def get_opening_average(self, weeks: int = OPENING_PERIOD_WEEKS) -> Decimal:
        """
        Get average price of first N weeks.

        Args:
            weeks: Number of weeks to average

        Returns:
            Average opening price

        Raises:
            InsufficientPriceDataError: If not enough data points
        """
        if len(self.prices) < weeks:
            raise InsufficientPriceDataError(
                f"Not enough data points. Need {weeks}, have {len(self.prices)}"
            )

        prices = [p[1] for p in self.prices[:weeks]]
        return sum(prices) / Decimal(len(prices))

    def get_current_average(self, weeks: int = CURRENT_PERIOD_WEEKS) -> Decimal:
        """
        Get average price of last N weeks.

        Args:
            weeks: Number of weeks to average

        Returns:
            Average current price

        Raises:
            InsufficientPriceDataError: If not enough data points
        """
        if len(self.prices) < weeks:
            raise InsufficientPriceDataError(
                f"Not enough data points. Need {weeks}, have {len(self.prices)}"
            )

        prices = [p[1] for p in self.prices[-weeks:]]
        return sum(prices) / Decimal(len(prices))

    def to_chart_data(self) -> list[dict[str, str | float]]:
        """
        Convert price data to chart format for frontend.

        Returns:
            List of dictionaries with 'x' (timestamp) and 'y' (price)
        """
        return [
            {"x": timestamp.strftime(DATE_TIME_FORMAT), "y": float(price)}
            for timestamp, price in self.prices
        ]
