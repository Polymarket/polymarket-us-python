"""Search type definitions."""

from typing import Literal, TypedDict

from polymarket_us.types.events import Event


class SearchParams(TypedDict, total=False):
    """Parameters for searching."""

    query: str
    limit: int
    seriesIds: list[int]
    status: Literal["active", "closed", "upcoming"]
    page: int


class SearchResponse(TypedDict):
    """Response from search."""

    events: list[Event]
