"""Series resource."""

from collections.abc import AsyncIterator, Iterator
from typing import Any

from polymarket_us.pagination import (
    DEFAULT_PAGE_SIZE,
    paginate_offset,
    paginate_offset_async,
)
from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import (
    GetSeriesListResponse,
    GetSeriesResponse,
    SeriesListParams,
)
from polymarket_us.types import (
    Series as SeriesType,
)


class Series(APIResource):
    """Series API resource."""

    def list(self, params: SeriesListParams | None = None) -> GetSeriesListResponse:
        """List series with optional filtering."""
        return self._client.get("/v1/series", query=dict(params) if params else None)

    def iterate(
        self,
        params: SeriesListParams | None = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Iterator[SeriesType]:
        """Iterate over all series across pages, fetching them lazily."""

        def fetch(offset: int, limit: int) -> dict[str, Any]:
            query: dict[str, Any] = dict(params) if params else {}
            query["limit"] = limit
            query["offset"] = offset
            return self._client.get("/v1/series", query=query)

        return paginate_offset(fetch, "series", page_size)

    def retrieve(self, id: int) -> GetSeriesResponse:
        """Get a series by ID."""
        return self._client.get(f"/v1/series/id/{id}")


class AsyncSeries(AsyncAPIResource):
    """Series API resource (async)."""

    async def list(self, params: SeriesListParams | None = None) -> GetSeriesListResponse:
        """List series with optional filtering."""
        return await self._client.get("/v1/series", query=dict(params) if params else None)

    def iterate(
        self,
        params: SeriesListParams | None = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncIterator[SeriesType]:
        """Iterate over all series across pages, fetching them lazily."""

        async def fetch(offset: int, limit: int) -> dict[str, Any]:
            query: dict[str, Any] = dict(params) if params else {}
            query["limit"] = limit
            query["offset"] = offset
            return await self._client.get("/v1/series", query=query)

        return paginate_offset_async(fetch, "series", page_size)

    async def retrieve(self, id: int) -> GetSeriesResponse:
        """Get a series by ID."""
        return await self._client.get(f"/v1/series/id/{id}")
