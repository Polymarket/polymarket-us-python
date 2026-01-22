"""Series resource."""

from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import GetSeriesListResponse, GetSeriesResponse, SeriesListParams


class Series(APIResource):
    """Series API resource."""

    def list(self, params: SeriesListParams | None = None) -> GetSeriesListResponse:
        """List series with optional filtering."""
        return self._client.get("/v1/series", query=dict(params) if params else None)

    def retrieve(self, id: int) -> GetSeriesResponse:
        """Get a series by ID."""
        return self._client.get(f"/v1/series/id/{id}")


class AsyncSeries(AsyncAPIResource):
    """Series API resource (async)."""

    async def list(self, params: SeriesListParams | None = None) -> GetSeriesListResponse:
        """List series with optional filtering."""
        return await self._client.get("/v1/series", query=dict(params) if params else None)

    async def retrieve(self, id: int) -> GetSeriesResponse:
        """Get a series by ID."""
        return await self._client.get(f"/v1/series/id/{id}")
