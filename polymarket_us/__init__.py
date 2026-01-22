"""Polymarket US Python SDK."""

from polymarket_us.async_client import AsyncPolymarketUS
from polymarket_us.client import PolymarketUS
from polymarket_us.errors import (
    APIError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PolymarketUSError,
    RateLimitError,
    WebSocketError,
)

__all__ = [
    # Clients
    "PolymarketUS",
    "AsyncPolymarketUS",
    # Errors
    "PolymarketUSError",
    "APIError",
    "AuthenticationError",
    "BadRequestError",
    "NotFoundError",
    "RateLimitError",
    "InternalServerError",
    "WebSocketError",
]

try:
    from importlib.metadata import version

    __version__ = version("polymarket-us")
except ImportError:
    # Fallback for Python < 3.8
    try:
        from importlib_metadata import version

        __version__ = version("polymarket-us")
    except ImportError:
        # Fallback if package not installed
        __version__ = "0.1.0"
