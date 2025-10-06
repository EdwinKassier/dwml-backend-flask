"""Unit tests for crypto service."""

import pytest
from unittest.mock import Mock, patch
from app.services.crypto_service import CryptoService


class TestCryptoService:
    """Test crypto service functionality."""
    
    def test_analyze_investment_success(self):
        """Test successful investment analysis."""
        service = CryptoService()
        
        with patch('app.services.crypto_service.DataCollector') as mock_collector, \
             patch('app.services.crypto_service.GraphCreator') as mock_creator:
            
            # Mock the collectors
            mock_collector_instance = Mock()
            mock_collector_instance.driver_logic.return_value = {"profit": 1000}
            mock_collector.return_value = mock_collector_instance
            
            mock_creator_instance = Mock()
            mock_creator_instance.driver_logic.return_value = [{"x": "2023-01-01", "y": 1000}]
            mock_creator.return_value = mock_creator_instance
            
            # Test the service
            result = service.analyze_investment("BTC", 1000)
            
            # Verify the result
            assert "message" in result
            assert "graph_data" in result
            assert result["message"] == {"profit": 1000}
            assert result["graph_data"] == [{"x": "2023-01-01", "y": 1000}]
    
    def test_analyze_investment_failure(self):
        """Test investment analysis failure."""
        service = CryptoService()
        
        with patch('app.services.crypto_service.DataCollector') as mock_collector:
            mock_collector_instance = Mock()
            mock_collector_instance.driver_logic.side_effect = Exception("API Error")
            mock_collector.return_value = mock_collector_instance
            
            # Test that exception is raised
            with pytest.raises(Exception, match="Analysis failed: API Error"):
                service.analyze_investment("BTC", 1000)
    
    def test_get_historical_data(self):
        """Test getting historical data."""
        service = CryptoService()
        
        with patch('app.services.crypto_service.DataCollector') as mock_collector:
            mock_collector_instance = Mock()
            mock_collector_instance.get_historical_data.return_value = [{"date": "2023-01-01", "price": 1000}]
            mock_collector.return_value = mock_collector_instance
            
            result = service.get_historical_data("BTC")
            
            assert result == [{"date": "2023-01-01", "price": 1000}]
    
    def test_calculate_profit(self):
        """Test profit calculation."""
        service = CryptoService()
        
        with patch('app.services.crypto_service.DataCollector') as mock_collector:
            mock_collector_instance = Mock()
            mock_collector_instance.calculate_profit.return_value = {"profit": 500}
            mock_collector.return_value = mock_collector_instance
            
            result = service.calculate_profit("BTC", 1000)
            
            assert result == {"profit": 500}
