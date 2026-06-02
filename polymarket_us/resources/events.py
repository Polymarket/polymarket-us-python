"""Events resource."""

from collections.abc import AsyncIterator, Iterator
from typing import Any

from polymarket_us.pagination import (
    DEFAULT_PAGE_SIZE,
    paginate_offset,
    paginate_offset_async,
)
from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import Event, EventsListParams, GetEventResponse, GetEventsResponse


class Events(APIResource):
    """Events API resource."""

    def list(self, params: EventsListParams | None = None) -> GetEventsResponse:
        """List events with optional filtering."""
        return self._client.get("/v1/events", query=dict(params) if params else None)

    def iterate(
        self,
        params: EventsListParams | None = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Iterator[Event]:
        """Iterate over all events across pages, fetching them lazily."""

        def fetch(offset: int, limit: int) -> dict[str, Any]:
            query: dict[str, Any] = dict(params) if params else {}
            query["limit"] = limit
            query["offset"] = offset
            return self._client.get("/v1/events", query=query)

        return paginate_offset(fetch, "events", page_size)

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

    def iterate(
        self,
        params: EventsListParams | None = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncIterator[Event]:
        """Iterate over all events across pages, fetching them lazily."""

        async def fetch(offset: int, limit: int) -> dict[str, Any]:
            query: dict[str, Any] = dict(params) if params else {}
            query["limit"] = limit
            query["offset"] = offset
            return await self._client.get("/v1/events", query=query)

        return paginate_offset_async(fetch, "events", page_size)

    async def retrieve(self, id: int) -> GetEventResponse:
        """Get an event by ID."""
        return await self._client.get(f"/v1/events/{id}")

    async def retrieve_by_slug(self, slug: str) -> GetEventResponse:
        """Get an event by slug."""
        return await self._client.get(f"/v1/events/slug/{slug}")
