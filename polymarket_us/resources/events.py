"""Events resource."""

from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import EventsListParams, GetEventResponse, GetEventsResponse


class Events(APIResource):
    """Events API resource."""

    def list(self, params: EventsListParams | None = None) -> GetEventsResponse:
        """List events with optional filtering.

        Args:
            params: Optional filtering and pagination parameters

        Returns:
            Response containing list of events
        """
        return self._client.get("/v1/events", query=self._convert_params(params))

    def retrieve(self, id: int) -> GetEventResponse:
        """Get an event by ID.

        Args:
            id: Event ID

        Returns:
            Response containing the event
        """
        return self._client.get(f"/v1/events/{id}")

    def retrieve_by_slug(self, slug: str) -> GetEventResponse:
        """Get an event by slug.

        Args:
            slug: Event slug

        Returns:
            Response containing the event
        """
        return self._client.get(f"/v1/events/slug/{slug}")


class AsyncEvents(AsyncAPIResource):
    """Events API resource (async)."""

    async def list(self, params: EventsListParams | None = None) -> GetEventsResponse:
        """List events with optional filtering.

        Args:
            params: Optional filtering and pagination parameters

        Returns:
            Response containing list of events
        """
        return await self._client.get("/v1/events", query=self._convert_params(params))

    async def retrieve(self, id: int) -> GetEventResponse:
        """Get an event by ID.

        Args:
            id: Event ID

        Returns:
            Response containing the event
        """
        return await self._client.get(f"/v1/events/{id}")

    async def retrieve_by_slug(self, slug: str) -> GetEventResponse:
        """Get an event by slug.

        Args:
            slug: Event slug

        Returns:
            Response containing the event
        """
        return await self._client.get(f"/v1/events/slug/{slug}")
