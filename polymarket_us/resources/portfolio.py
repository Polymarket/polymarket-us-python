"""Portfolio resource."""

from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import (
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
