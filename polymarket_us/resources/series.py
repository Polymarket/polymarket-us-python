"""Series resource."""

from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import GetSeriesListResponse, GetSeriesResponse, SeriesListParams


class Series(APIResource):
    """Series API resource."""

    def list(self, params: SeriesListParams | None = None) -> GetSeriesListResponse:
        """List series with optional filtering.

        Args:
            params: Optional filtering and pagination parameters

        Returns:
            Response containing list of series
        """
        return self._client.get("/v1/series", query=self._convert_params(params))

    def retrieve(self, id: int) -> GetSeriesResponse:
        """Get a series by ID.

        Args:
            id: Series ID

        Returns:
            Response containing the series
        """
        return self._client.get(f"/v1/series/id/{id}")


class AsyncSeries(AsyncAPIResource):
    """Series API resource (async)."""

    async def list(self, params: SeriesListParams | None = None) -> GetSeriesListResponse:
        """List series with optional filtering.

        Args:
            params: Optional filtering and pagination parameters

        Returns:
            Response containing list of series
        """
        return await self._client.get("/v1/series", query=self._convert_params(params))

    async def retrieve(self, id: int) -> GetSeriesResponse:
        """Get a series by ID.

        Args:
            id: Series ID

        Returns:
            Response containing the series
        """
        return await self._client.get(f"/v1/series/id/{id}")
