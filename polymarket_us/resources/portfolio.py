"""Portfolio resource."""

from collections.abc import AsyncIterator, Iterator
from typing import Any

from polymarket_us.pagination import paginate_cursor, paginate_cursor_async
from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import (
    Activity,
    GetActivitiesParams,
    GetActivitiesResponse,
    GetUserPositionsParams,
    GetUserPositionsResponse,
)


class Portfolio(APIResource):
    """Portfolio API resource (requires authentication)."""

    def positions(self, params: GetUserPositionsParams | None = None) -> GetUserPositionsResponse:
        """Get trading positions."""
        return self._client.get(
            "/v1/portfolio/positions",
            query=dict(params) if params else None,
            authenticated=True,
        )

    def activities(self, params: GetActivitiesParams | None = None) -> GetActivitiesResponse:
        """Get activity history."""
        return self._client.get(
            "/v1/portfolio/activities",
            query=dict(params) if params else None,
            authenticated=True,
        )

    def iterate_activities(self, params: GetActivitiesParams | None = None) -> Iterator[Activity]:
        """Iterate over all activities, following the cursor across pages."""

        def fetch(cursor: str | None) -> dict[str, Any]:
            query: dict[str, Any] = dict(params) if params else {}
            if cursor:
                query["cursor"] = cursor
            return self._client.get("/v1/portfolio/activities", query=query, authenticated=True)

        return paginate_cursor(fetch, "activities")


class AsyncPortfolio(AsyncAPIResource):
    """Portfolio API resource (async, requires authentication)."""

    async def positions(
        self, params: GetUserPositionsParams | None = None
    ) -> GetUserPositionsResponse:
        """Get trading positions."""
        return await self._client.get(
            "/v1/portfolio/positions",
            query=dict(params) if params else None,
            authenticated=True,
        )

    async def activities(self, params: GetActivitiesParams | None = None) -> GetActivitiesResponse:
        """Get activity history."""
        return await self._client.get(
            "/v1/portfolio/activities",
            query=dict(params) if params else None,
            authenticated=True,
        )

    def iterate_activities(
        self, params: GetActivitiesParams | None = None
    ) -> AsyncIterator[Activity]:
        """Iterate over all activities, following the cursor across pages."""

        async def fetch(cursor: str | None) -> dict[str, Any]:
            query: dict[str, Any] = dict(params) if params else {}
            if cursor:
                query["cursor"] = cursor
            return await self._client.get(
                "/v1/portfolio/activities", query=query, authenticated=True
            )

        return paginate_cursor_async(fetch, "activities")
