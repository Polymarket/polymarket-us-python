"""Markets resource."""

from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import (
    GetMarketResponse,
    GetMarketsResponse,
    MarketBBO,
    MarketBook,
    MarketSettlement,
    MarketsListParams,
)


class Markets(APIResource):
    """Markets API resource."""

    def list(self, params: MarketsListParams | None = None) -> GetMarketsResponse:
        """List markets with optional filtering."""
        return self._client.get("/v1/markets", query=dict(params) if params else None)

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
