"""API endpoints module."""

from .crypto import core as crypto_bp
from .health import health as health_bp

__all__ = ["crypto_bp", "health_bp"]
