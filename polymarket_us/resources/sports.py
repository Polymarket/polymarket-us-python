"""Sports resource."""

from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import (
    GetSportsResponse,
    GetSportsTeamsParams,
    GetSportsTeamsResponse,
)


class Sports(APIResource):
    """Sports API resource."""

    def list(self) -> GetSportsResponse:
        """List all sports.

        Returns:
            Response containing list of sports
        """
        return self._client.get("/v1/sports")

    def teams(self, params: GetSportsTeamsParams | None = None) -> GetSportsTeamsResponse:
        """Get teams for a provider.

        Args:
            params: Optional parameters to filter teams

        Returns:
            Response containing teams
        """
        return self._client.get("/v1/sports/teams/provider", query=self._convert_params(params))


class AsyncSports(AsyncAPIResource):
    """Sports API resource (async)."""

    async def list(self) -> GetSportsResponse:
        """List all sports.

        Returns:
            Response containing list of sports
        """
        return await self._client.get("/v1/sports")

    async def teams(self, params: GetSportsTeamsParams | None = None) -> GetSportsTeamsResponse:
        """Get teams for a provider.

        Args:
            params: Optional parameters to filter teams

        Returns:
            Response containing teams
        """
        return await self._client.get(
            "/v1/sports/teams/provider", query=self._convert_params(params)
        )
