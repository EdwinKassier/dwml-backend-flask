"""Domain services containing business logic."""
import logging
from decimal import Decimal
from typing import Any, Dict

from .exceptions import SymbolNotFoundError
from .models import Investment

logger = logging.getLogger(__name__)


class CryptoAnalysisService:
    """
    Core business logic for crypto investment analysis.

    This service orchestrates repositories and applies business rules
    for analyzing cryptocurrency investments.
    """

    def __init__(self, price_repo: Any, investment_repo: Any) -> None:
        """
        Initialize service with repository dependencies.

        Args:
            price_repo: Repository for price data access
            investment_repo: Repository for investment logging
        """
        self._price_repo = price_repo
        self._investment_repo = investment_repo

    def analyze_investment(self, symbol: str, amount: Decimal) -> Dict[str, Any]:
        """
        Analyze a crypto investment.

        This is the core use case orchestration that:
        1. Creates and validates investment
        2. Checks symbol exists
        3. Fetches price data
        4. Calculates profit metrics
        5. Logs the query
        6. Returns results

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC')
            amount: Investment amount in USD

        Returns:
            Dictionary with analysis results including:
            - SYMBOL: Normalized symbol
            - INVESTMENT: Investment amount
            - NUMBERCOINS: Number of coins purchased
            - PROFIT: Profit/loss amount
            - GROWTHFACTOR: Growth factor ratio
            - LAMBOS: Lamborghini equivalent
            - GENERATIONDATE: Analysis timestamp
            - graph_data: Historical price data for charting

        Raises:
            InvalidInvestmentError: If investment data is invalid
            SymbolNotFoundError: If symbol doesn't exist on exchange
            InsufficientPriceDataError: If not enough price data
            ExternalServiceError: If external API fails
        """
        logger.info(f"Analyzing investment: {symbol}, amount: {amount}")

        # 1. Create and validate domain model
        investment = Investment(symbol=symbol, amount=amount)

        # 2. Check if symbol exists on exchange
        if not self._price_repo.symbol_exists(investment.symbol):
            logger.warning(f"Symbol not found: {investment.symbol}")
            raise SymbolNotFoundError(
                f"Symbol {investment.symbol} not found on exchange"
            )

        # 3. Get price data (handles caching internally)
        price_data = self._price_repo.get_price_data(investment.symbol)

        # 4. Calculate metrics using domain model methods
        opening_avg = price_data.get_opening_average()
        current_avg = price_data.get_current_average()

        coins = investment.calculate_coins_purchased(opening_avg)
        profit = investment.calculate_profit(opening_avg, current_avg)
        growth = investment.calculate_growth_factor(opening_avg, current_avg)
        lambos = investment.calculate_lambos(opening_avg, current_avg)

        # 5. Log the query to database
        self._investment_repo.log_query(investment)

        # 6. Build and return result
        result = {
            "SYMBOL": investment.symbol,
            "INVESTMENT": float(investment.amount),
            "NUMBERCOINS": float(coins),
            "PROFIT": float(profit),
            "GROWTHFACTOR": float(growth),
            "LAMBOS": float(lambos),
            "GENERATIONDATE": investment.created_at.isoformat(),
            "graph_data": price_data.to_chart_data(),
        }

        logger.info(
            f"Analysis complete for {symbol}: profit={profit:.2f}, lambos={lambos:.2f}"
        )
        return result
