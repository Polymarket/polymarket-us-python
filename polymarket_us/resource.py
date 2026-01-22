"""Base resource classes."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from polymarket_us.async_client import AsyncPolymarketUS
    from polymarket_us.client import PolymarketUS


class APIResource:
    """Base class for API resources (sync)."""

    def __init__(self, client: PolymarketUS) -> None:
        self._client = client


class AsyncAPIResource:
    """Base class for API resources (async)."""

    def __init__(self, client: AsyncPolymarketUS) -> None:
        self._client = client
