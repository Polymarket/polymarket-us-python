"""Events type definitions."""

from typing import Literal, TypedDict

from polymarket_us.types.common import PaginationParams


class SeriesInfo(TypedDict, total=False):
    """Series information within an event."""

    id: int
    slug: str
    title: str


class Tag(TypedDict):
    """Event tag."""

    id: int
    slug: str
    label: str


class Market(TypedDict, total=False):
    """Market within an event."""

    id: int
    slug: str
    title: str
    outcome: str
    active: bool
    closed: bool
    liquidity: float
    volume: float


class Event(TypedDict, total=False):
    """Event details."""

    id: int
    slug: str
    title: str
    description: str
    start_time: str
    end_time: str
    active: bool
    closed: bool
    archived: bool
    featured: bool
    liquidity: float
    volume: float
    markets: list[Market]
    tags: list[Tag]
    series: SeriesInfo


class EventsListParams(PaginationParams, total=False):
    """Parameters for listing events."""

    order_by: list[str]
    order_direction: Literal["asc", "desc"]
    id: list[int]
    slug: list[str]
    archived: bool
    active: bool
    closed: bool
    liquidity_min: float
    liquidity_max: float
    volume_min: float
    volume_max: float
    start_date_min: str
    start_date_max: str
    end_date_min: str
    end_date_max: str
    tag_id: int
    tag_slug: str
    related_tags: bool
    featured: bool
    series_id: list[int]
    event_date: str
    event_week: int
    start_time_min: str
    start_time_max: str
    game_id: int
    ended: bool
    categories: list[str]


class GetEventsResponse(TypedDict):
    """Response for listing events."""

    events: list[Event]


class GetEventResponse(TypedDict):
    """Response for getting a single event."""

    event: Event
