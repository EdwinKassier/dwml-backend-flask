"""Unit tests for data models."""

import pytest
from datetime import datetime
from app.models.crypto_models import (
    CryptoAnalysisResult,
    PriceDataPoint,
    GraphData,
    InvestmentAnalysis,
)


class TestCryptoAnalysisResult:
    """Test CryptoAnalysisResult model."""

    def test_crypto_analysis_result_creation(self):
        """Test creating a crypto analysis result."""
        result = CryptoAnalysisResult(
            symbol="BTC",
            investment=1000,
            number_coins=0.1,
            profit=500,
            growth_factor=1.5,
            lambos=2.5,
            generation_date="2023-01-01",
        )

        assert result.symbol == "BTC"
        assert result.investment == 1000
        assert result.number_coins == 0.1
        assert result.profit == 500
        assert result.growth_factor == 1.5
        assert result.lambos == 2.5
        assert result.generation_date == "2023-01-01"

    def test_crypto_analysis_result_to_dict(self):
        """Test converting to dictionary."""
        result = CryptoAnalysisResult(
            symbol="BTC",
            investment=1000,
            number_coins=0.1,
            profit=500,
            growth_factor=1.5,
            lambos=2.5,
            generation_date="2023-01-01",
        )

        data = result.to_dict()

        assert data["SYMBOL"] == "BTC"
        assert data["INVESTMENT"] == 1000
        assert data["NUMBERCOINS"] == 0.1
        assert data["PROFIT"] == 500
        assert data["GROWTHFACTOR"] == 1.5
        assert data["LAMBOS"] == 2.5
        assert data["GENERATIONDATE"] == "2023-01-01"


class TestPriceDataPoint:
    """Test PriceDataPoint model."""

    def test_price_data_point_creation(self):
        """Test creating a price data point."""
        point = PriceDataPoint(timestamp="2023-01-01", price=1000.0, volume=100.0)

        assert point.timestamp == "2023-01-01"
        assert point.price == 1000.0
        assert point.volume == 100.0

    def test_price_data_point_to_dict(self):
        """Test converting to dictionary."""
        point = PriceDataPoint(timestamp="2023-01-01", price=1000.0)

        data = point.to_dict()

        assert data["x"] == "2023-01-01"
        assert data["y"] == 1000.0


class TestGraphData:
    """Test GraphData model."""

    def test_graph_data_creation(self):
        """Test creating graph data."""
        points = [
            PriceDataPoint("2023-01-01", 1000.0),
            PriceDataPoint("2023-01-02", 1050.0),
        ]

        graph_data = GraphData(data_points=points, symbol="BTC", time_range="1D")

        assert len(graph_data.data_points) == 2
        assert graph_data.symbol == "BTC"
        assert graph_data.time_range == "1D"

    def test_graph_data_to_list(self):
        """Test converting to list."""
        points = [
            PriceDataPoint("2023-01-01", 1000.0),
            PriceDataPoint("2023-01-02", 1050.0),
        ]

        graph_data = GraphData(points, "BTC", "1D")
        data_list = graph_data.to_list()

        assert len(data_list) == 2
        assert data_list[0]["x"] == "2023-01-01"
        assert data_list[0]["y"] == 1000.0
        assert data_list[1]["x"] == "2023-01-02"
        assert data_list[1]["y"] == 1050.0


class TestInvestmentAnalysis:
    """Test InvestmentAnalysis model."""

    def test_investment_analysis_creation(self):
        """Test creating investment analysis."""
        result = CryptoAnalysisResult("BTC", 1000, 0.1, 500, 1.5, 2.5, "2023-01-01")
        graph_data = GraphData([PriceDataPoint("2023-01-01", 1000.0)], "BTC", "1D")

        analysis = InvestmentAnalysis(
            analysis_result=result, graph_data=graph_data, success=True
        )

        assert analysis.analysis_result == result
        assert analysis.graph_data == graph_data
        assert analysis.success is True
        assert analysis.error_message is None

    def test_investment_analysis_to_dict(self):
        """Test converting to dictionary."""
        result = CryptoAnalysisResult("BTC", 1000, 0.1, 500, 1.5, 2.5, "2023-01-01")
        graph_data = GraphData([PriceDataPoint("2023-01-01", 1000.0)], "BTC", "1D")

        analysis = InvestmentAnalysis(result, graph_data, True)
        data = analysis.to_dict()

        assert "message" in data
        assert "graph_data" in data
        assert "success" in data
        assert data["success"] is True
