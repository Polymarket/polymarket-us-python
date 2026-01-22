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
        """Get trading positions.

        Args:
            params: Optional filtering parameters

        Returns:
            Response containing positions
        """
        return self._client.get(
            "/v1/portfolio/positions",
            query=self._convert_params(params),
            authenticated=True,
        )

    def activities(self, params: GetActivitiesParams | None = None) -> GetActivitiesResponse:
        """Get activity history.

        Args:
            params: Optional filtering parameters

        Returns:
            Response containing activities
        """
        return self._client.get(
            "/v1/portfolio/activities",
            query=self._convert_params(params),
            authenticated=True,
        )


class AsyncPortfolio(AsyncAPIResource):
    """Portfolio API resource (async, requires authentication)."""

    async def positions(
        self, params: GetUserPositionsParams | None = None
    ) -> GetUserPositionsResponse:
        """Get trading positions.

        Args:
            params: Optional filtering parameters

        Returns:
            Response containing positions
        """
        return await self._client.get(
            "/v1/portfolio/positions",
            query=self._convert_params(params),
            authenticated=True,
        )

    async def activities(self, params: GetActivitiesParams | None = None) -> GetActivitiesResponse:
        """Get activity history.

        Args:
            params: Optional filtering parameters

        Returns:
            Response containing activities
        """
        return await self._client.get(
            "/v1/portfolio/activities",
            query=self._convert_params(params),
            authenticated=True,
        )
