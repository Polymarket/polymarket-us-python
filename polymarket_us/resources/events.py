"""Events resource."""

from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import EventsListParams, GetEventResponse, GetEventsResponse


class Events(APIResource):
    """Events API resource."""

    def list(self, params: EventsListParams | None = None) -> GetEventsResponse:
        """List events with optional filtering."""
        return self._client.get("/v1/events", query=dict(params) if params else None)

    def retrieve(self, id: int) -> GetEventResponse:
        """Get an event by ID."""
        return self._client.get(f"/v1/events/{id}")

    def retrieve_by_slug(self, slug: str) -> GetEventResponse:
        """Get an event by slug."""
        return self._client.get(f"/v1/events/slug/{slug}")


class AsyncEvents(AsyncAPIResource):
    """Events API resource (async)."""

    async def list(self, params: EventsListParams | None = None) -> GetEventsResponse:
        """List events with optional filtering."""
        return await self._client.get("/v1/events", query=dict(params) if params else None)

    async def retrieve(self, id: int) -> GetEventResponse:
        """Get an event by ID."""
        return await self._client.get(f"/v1/events/{id}")

    async def retrieve_by_slug(self, slug: str) -> GetEventResponse:
        """Get an event by slug."""
        return await self._client.get(f"/v1/events/slug/{slug}")
