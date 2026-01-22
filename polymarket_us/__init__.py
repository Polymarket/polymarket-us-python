"""Polymarket US Python SDK."""

from polymarket_us.async_client import AsyncPolymarketUS
from polymarket_us.client import PolymarketUS
from polymarket_us.errors import (
    APIConnectionError,
    APIError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
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
    "APIConnectionError",
    "APITimeoutError",
    "APIStatusError",
    "AuthenticationError",
    "BadRequestError",
    "PermissionDeniedError",
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
