"""Search resource."""

from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import SearchParams, SearchResponse


class Search(APIResource):
    """Search API resource."""

    def query(self, params: SearchParams | None = None) -> SearchResponse:
        """Search for events.

        Args:
            params: Optional search parameters

        Returns:
            Response containing matching events
        """
        return self._client.get("/v1/search", query=self._convert_params(params))


class AsyncSearch(AsyncAPIResource):
    """Search API resource (async)."""

    async def query(self, params: SearchParams | None = None) -> SearchResponse:
        """Search for events.

        Args:
            params: Optional search parameters

        Returns:
            Response containing matching events
        """
        return await self._client.get("/v1/search", query=self._convert_params(params))
