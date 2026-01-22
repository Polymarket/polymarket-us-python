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
    startTime: str
    endTime: str
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

    orderBy: list[str]
    orderDirection: Literal["asc", "desc"]
    id: list[int]
    slug: list[str]
    archived: bool
    active: bool
    closed: bool
    liquidityMin: float
    liquidityMax: float
    volumeMin: float
    volumeMax: float
    startDateMin: str
    startDateMax: str
    endDateMin: str
    endDateMax: str
    tagId: int
    tagSlug: str
    relatedTags: bool
    featured: bool
    seriesId: list[int]
    eventDate: str
    eventWeek: int
    startTimeMin: str
    startTimeMax: str
    gameId: int
    ended: bool
    categories: list[str]


class GetEventsResponse(TypedDict):
    """Response for listing events."""

    events: list[Event]


class GetEventResponse(TypedDict):
    """Response for getting a single event."""

    event: Event
