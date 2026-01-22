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

__version__ = "0.1.0"
