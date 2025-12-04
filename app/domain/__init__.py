"""Domain - DWML application business logic."""

from .exceptions import (
    CryptoDomainError,
    ExternalServiceError,
    InsufficientPriceDataError,
    InvalidInvestmentError,
    SymbolNotFoundError,
)
from .graphql_schema import schema
from .models import Investment, PriceData
from .schemas import (
    CryptoAnalysisRequestSchema,
    CryptoAnalysisResponseSchema,
    ErrorResponseSchema,
    HealthCheckSchema,
    validate_crypto_request,
    validate_health_response,
)
from .services import CryptoAnalysisService

# Import tasks for Celery autodiscovery
try:
    from . import tasks  # noqa: F401
except ImportError:
    # Celery might not be available
    pass

from app.shared import shared_db

from .repositories import KrakenPriceRepository, SqlAlchemyInvestmentRepository

# Initialize repositories
price_repo = KrakenPriceRepository(shared_db)
investment_repo = SqlAlchemyInvestmentRepository(shared_db)

__all__ = [
    "Investment",
    "PriceData",
    "CryptoAnalysisService",
    "CryptoDomainError",
    "InvalidInvestmentError",
    "SymbolNotFoundError",
    "InsufficientPriceDataError",
    "ExternalServiceError",
    "CryptoAnalysisRequestSchema",
    "CryptoAnalysisResponseSchema",
    "HealthCheckSchema",
    "ErrorResponseSchema",
    "validate_crypto_request",
    "validate_health_response",
    "schema",
    "price_repo",
    "investment_repo",
]
