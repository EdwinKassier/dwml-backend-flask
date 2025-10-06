"""Crypto investment analysis service."""

from typing import Dict, List, Any
from ..utils.data_collector import DataCollector
from ..utils.graph_creator import GraphCreator


class CryptoService:
    """Service for crypto investment analysis."""

    def __init__(self):
        self.data_collector = None
        self.graph_creator = None

    def analyze_investment(self, symbol: str, investment: int) -> Dict[str, Any]:
        """
        Analyze crypto investment and return results.

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC')
            investment: Investment amount in USD

        Returns:
            Dict containing analysis results and graph data
        """
        try:
            # Initialize collectors
            self.data_collector = DataCollector(symbol, investment)
            self.graph_creator = GraphCreator(symbol)

            # Get analysis results
            analysis_result = self.data_collector.driver_logic()
            graph_data = self.graph_creator.driver_logic()

            return {"message": analysis_result, "graph_data": graph_data}

        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")

    def get_historical_data(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Get historical price data for a symbol.

        Args:
            symbol: Cryptocurrency symbol

        Returns:
            List of historical data points
        """
        try:
            collector = DataCollector(
                symbol, 0
            )  # No investment needed for historical data
            return collector.get_historical_data()
        except Exception as e:
            raise Exception(f"Failed to get historical data: {str(e)}")

    def calculate_profit(self, symbol: str, investment: int) -> Dict[str, Any]:
        """
        Calculate profit for a crypto investment.

        Args:
            symbol: Cryptocurrency symbol
            investment: Investment amount

        Returns:
            Dict containing profit calculations
        """
        try:
            collector = DataCollector(symbol, investment)
            return collector.calculate_profit()
        except Exception as e:
            raise Exception(f"Profit calculation failed: {str(e)}")
