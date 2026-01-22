"""Common type definitions."""

from typing import Literal, TypedDict


class Amount(TypedDict):
    """Monetary amount."""

    value: str
    currency: Literal["USD"]


class PaginationParams(TypedDict, total=False):
    """Pagination parameters."""

    limit: int
    offset: int
