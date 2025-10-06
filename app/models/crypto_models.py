"""Data models for crypto analysis."""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class CryptoAnalysisResult:
    """Result of crypto investment analysis."""

    symbol: str
    investment: int
    number_coins: float
    profit: float
    growth_factor: float
    lambos: float
    generation_date: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "SYMBOL": self.symbol,
            "INVESTMENT": self.investment,
            "NUMBERCOINS": self.number_coins,
            "PROFIT": self.profit,
            "GROWTHFACTOR": self.growth_factor,
            "LAMBOS": self.lambos,
            "GENERATIONDATE": self.generation_date,
        }


@dataclass
class PriceDataPoint:
    """Single price data point."""

    timestamp: str
    price: float
    volume: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {"x": self.timestamp, "y": self.price}


@dataclass
class GraphData:
    """Graph data for visualization."""

    data_points: List[PriceDataPoint]
    symbol: str
    time_range: str

    def to_list(self) -> List[dict]:
        """Convert to list of dictionaries for JSON serialization."""
        return [point.to_dict() for point in self.data_points]


@dataclass
class InvestmentAnalysis:
    """Complete investment analysis."""

    analysis_result: CryptoAnalysisResult
    graph_data: GraphData
    success: bool
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "message": self.analysis_result.to_dict(),
            "graph_data": self.graph_data.to_list(),
            "success": self.success,
            "error": self.error_message,
        }
