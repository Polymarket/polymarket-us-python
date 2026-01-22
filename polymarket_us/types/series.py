"""Series type definitions."""

from typing import Literal, TypedDict

from polymarket_us.types.common import PaginationParams


class Series(TypedDict, total=False):
    """Series details."""

    id: int
    slug: str
    title: str
    description: str
    active: bool
    closed: bool
    archived: bool
    recurrence: str


class SeriesListParams(PaginationParams, total=False):
    """Parameters for listing series."""

    order_by: list[str]
    order_direction: Literal["asc", "desc"]
    slug: list[str]
    archived: bool
    active: bool
    closed: bool
    recurrence: str


class GetSeriesListResponse(TypedDict):
    """Response for listing series."""

    series: list[Series]


class GetSeriesResponse(TypedDict):
    """Response for getting a single series."""

    series: Series
