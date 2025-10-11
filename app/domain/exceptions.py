"""Domain-specific exceptions for crypto investment analysis."""


class CryptoDomainError(Exception):
    """Base exception for crypto domain errors."""


class InvalidInvestmentError(CryptoDomainError):
    """Raised when investment data is invalid."""


class SymbolNotFoundError(CryptoDomainError):
    """Raised when cryptocurrency symbol doesn't exist on exchange."""


class InsufficientPriceDataError(CryptoDomainError):
    """Raised when there isn't enough price data for analysis."""


class ExternalServiceError(CryptoDomainError):
    """Raised when external API service fails."""
