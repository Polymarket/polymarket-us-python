"""Markets resource."""

from collections.abc import AsyncIterator, Iterator
from typing import Any

from polymarket_us.pagination import (
    DEFAULT_PAGE_SIZE,
    paginate_offset,
    paginate_offset_async,
)
from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import (
    GetMarketResponse,
    GetMarketsResponse,
    MarketBBO,
    MarketBook,
    MarketDetail,
    MarketSettlement,
    MarketsListParams,
)


class Markets(APIResource):
    """Markets API resource."""

    def list(self, params: MarketsListParams | None = None) -> GetMarketsResponse:
        """List markets with optional filtering."""
        return self._client.get("/v1/markets", query=dict(params) if params else None)

    def iterate(
        self,
        params: MarketsListParams | None = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Iterator[MarketDetail]:
        """Iterate over all markets across pages, fetching them lazily."""

        def fetch(offset: int, limit: int) -> dict[str, Any]:
            query: dict[str, Any] = dict(params) if params else {}
            query["limit"] = limit
            query["offset"] = offset
            return self._client.get("/v1/markets", query=query)

        return paginate_offset(fetch, "markets", page_size)

    def retrieve(self, id: int) -> GetMarketResponse:
        """Get a market by ID."""
        return self._client.get(f"/v1/market/id/{id}")

    def retrieve_by_slug(self, slug: str) -> GetMarketResponse:
        """Get a market by slug."""
        return self._client.get(f"/v1/market/slug/{slug}")

    def book(self, slug: str) -> MarketBook:
        """Get order book for a market."""
        return self._client.get(f"/v1/markets/{slug}/book")

    def bbo(self, slug: str) -> MarketBBO:
        """Get best bid/offer for a market."""
        return self._client.get(f"/v1/markets/{slug}/bbo")

    def settlement(self, slug: str) -> MarketSettlement:
        """Get settlement information for a market."""
        return self._client.get(f"/v1/markets/{slug}/settlement")


class AsyncMarkets(AsyncAPIResource):
    """Markets API resource (async)."""

    async def list(self, params: MarketsListParams | None = None) -> GetMarketsResponse:
        """List markets with optional filtering."""
        return await self._client.get("/v1/markets", query=dict(params) if params else None)

    def iterate(
        self,
        params: MarketsListParams | None = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncIterator[MarketDetail]:
        """Iterate over all markets across pages, fetching them lazily."""

        async def fetch(offset: int, limit: int) -> dict[str, Any]:
            query: dict[str, Any] = dict(params) if params else {}
            query["limit"] = limit
            query["offset"] = offset
            return await self._client.get("/v1/markets", query=query)

        return paginate_offset_async(fetch, "markets", page_size)

    async def retrieve(self, id: int) -> GetMarketResponse:
        """Get a market by ID."""
        return await self._client.get(f"/v1/market/id/{id}")

    async def retrieve_by_slug(self, slug: str) -> GetMarketResponse:
        """Get a market by slug."""
        return await self._client.get(f"/v1/market/slug/{slug}")

    async def book(self, slug: str) -> MarketBook:
        """Get order book for a market."""
        return await self._client.get(f"/v1/markets/{slug}/book")

    async def bbo(self, slug: str) -> MarketBBO:
        """Get best bid/offer for a market."""
        return await self._client.get(f"/v1/markets/{slug}/bbo")

    async def settlement(self, slug: str) -> MarketSettlement:
        """Get settlement information for a market."""
        return await self._client.get(f"/v1/markets/{slug}/settlement")
