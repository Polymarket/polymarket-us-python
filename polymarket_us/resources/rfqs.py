"""RFQ resource."""

from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import GetRFQTradesParams, GetRFQTradesResponse


class RFQs(APIResource):
    """RFQ API resource (requires authentication and RFQ access)."""

    def trades(self, params: GetRFQTradesParams | None = None) -> GetRFQTradesResponse:
        """Get a page of anonymous original RFQ fills, newest first."""
        return self._client.get(
            "/v1/rfqs/trades",
            query=dict(params) if params else None,
            authenticated=True,
        )


class AsyncRFQs(AsyncAPIResource):
    """RFQ API resource (async, requires authentication and RFQ access)."""

    async def trades(self, params: GetRFQTradesParams | None = None) -> GetRFQTradesResponse:
        """Get a page of anonymous original RFQ fills, newest first."""
        return await self._client.get(
            "/v1/rfqs/trades",
            query=dict(params) if params else None,
            authenticated=True,
        )
