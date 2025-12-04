"""Infrastructure repositories implementation."""

import logging
import random
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

import pandas as pd
import requests
from sqlalchemy.orm import Session

from app.domain.exceptions import InsufficientPriceDataError, SymbolNotFoundError
from app.domain.models import Investment, Logging, OpeningAverage, PriceData, Results
from app.shared.database import Database

logger = logging.getLogger(__name__)


class KrakenPriceRepository:
    """Repository for fetching price data from Kraken API."""

    def __init__(self, database: Database):
        self.db = database
        self.base_url = "https://api.kraken.com/0/public/OHLC"

    def symbol_exists(self, symbol: str) -> bool:
        """Check if symbol exists on exchange."""
        try:
            response = requests.get(
                f"{self.base_url}?pair={symbol}USD&interval=21600&since=1548111600"
            )
            data = response.json()

            if "error" in data and data["error"]:
                # Check specifically for "Instrument not found" or similar errors
                # Kraken returns errors as a list of strings
                for error in data["error"]:
                    if "Unknown asset pair" in error or "Instrument not found" in error:
                        return False

            # If result is empty or error present but not specific, might be other issue
            # But for "exists" check, if we get a result, it exists.
            if "result" in data and data["result"]:
                return True

            return False
        except Exception as e:
            logger.error(f"Error checking symbol existence: {e}")
            return False

    def get_price_data(self, symbol: str) -> PriceData:
        """Get historical price data for a symbol."""
        # 1. Check cache for opening average (optimization from original code)
        # The original code cached the opening average.
        # Here we are asked to return PriceData which contains a list of prices.
        # The service then calculates averages.
        # To be faithful to the original logic while fitting the new architecture,
        # we should fetch the full data.

        # However, the original code had a specific optimization:
        # if dataCache.check_if_historical_cache_exists(): use cached average
        # else: fetch from API and cache it.

        # The new PriceData model expects a list of (datetime, Decimal).
        # If we want to use the cache, we might need to adjust the repository
        # to return the averages directly or construct PriceData differently.

        # For now, let's implement fetching from Kraken as that's the primary source.
        # We can add caching of the *opening average* as a side effect if needed,
        # but the Service calculates it from the PriceData.

        # Let's fetch the data.
        try:
            url = f"{self.base_url}?pair={symbol}USD&interval=21600&since=1548111600"
            response = requests.get(url)
            data = response.json()

            if "error" in data and data["error"]:
                raise SymbolNotFoundError(
                    f"Error fetching data for {symbol}: {data['error']}"
                )

            if "result" not in data:
                raise InsufficientPriceDataError(f"No result data for {symbol}")

            # Kraken returns a dict where the key is the pair name
            # e.g. {'result': {'XXBTZUSD': [[...], ...]}}
            # We need to get the first value from the result dict
            result_data = list(data["result"].values())[0]

            # Convert to list of (datetime, Decimal)
            # Kraken OHLC format: [time, open, high, low, close, vwap, volume, count]
            prices = []
            for entry in result_data:
                # entry[0] is timestamp, entry[4] is close price
                timestamp = datetime.fromtimestamp(entry[0])
                close_price = Decimal(str(entry[4]))
                prices.append((timestamp, close_price))

            return PriceData(symbol=symbol, prices=prices)

        except Exception as e:
            logger.error(f"Error fetching price data: {e}")
            raise InsufficientPriceDataError(f"Failed to fetch price data: {e}")


class SqlAlchemyInvestmentRepository:
    """Repository for logging investments using SQLAlchemy."""

    def __init__(self, database: Database):
        self.db = database

    def log_query(self, investment: Investment) -> None:
        """Log investment query to database."""
        session = self.db.get_session()
        try:
            # Log to LOGGING table
            log_entry = Logging(
                SYMBOL=investment.symbol,
                INVESTMENT=float(investment.amount),
                GENERATIONDATE=investment.created_at,
                QUERY_ID=random.randint(1, 2147483647),
            )
            session.add(log_entry)

            # Also log to RESULTS table as per original code?
            # The original code logged to RESULTS in `create_result_dict` -> `insert_into_result`
            # But the Service builds the result dict.
            # The Service calls `log_query` at step 5.
            # We can log to RESULTS here if we had the profit metrics.
            # But `log_query` only takes `Investment`.

            # The original code had `dataCache.insert_into_logging()` at the start
            # and `dataCache.insert_into_result(final_result)` at the end.

            # The current Service only calls `log_query(investment)`.
            # If we want to log results, we might need to update the Service or the Repository interface.
            # However, I should stick to implementing the existing interface.

            session.commit()
        except Exception as e:
            logger.error(f"Error logging query: {e}")
            session.rollback()
        finally:
            session.close()
