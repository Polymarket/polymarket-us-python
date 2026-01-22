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
    from importlib.metadata import version as _version

    __version__ = _version("polymarket-us")
except Exception:
    __version__ = "0.1.0"
