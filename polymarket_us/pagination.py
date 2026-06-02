"""Auto-pagination helpers for list endpoints.

The API uses two pagination styles:

- cursor-based (``next_cursor`` / ``eof``) for activities and positions, and
- offset-based (bare array responses) for events, markets, series, and tags.

These helpers transparently walk all pages and yield individual items.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from typing import Any

DEFAULT_PAGE_SIZE = 100


def paginate_offset(
    fetch: Callable[[int, int], dict[str, Any]],
    items_key: str,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> Iterator[Any]:
    """Yield items across offset-paginated pages until a short page is returned."""
    offset = 0
    while True:
        page = fetch(offset, page_size)
        items = page.get(items_key) or []
        yield from items
        if len(items) < page_size:
            return
        offset += page_size


def paginate_cursor(
    fetch: Callable[[str | None], dict[str, Any]],
    items_key: str,
) -> Iterator[Any]:
    """Yield items across cursor-paginated pages until ``eof`` or no next cursor."""
    cursor: str | None = None
    while True:
        page = fetch(cursor)
        items = page.get(items_key) or []
        yield from items
        if page.get("eof"):
            return
        cursor = page.get("nextCursor")
        if not cursor:
            return


async def paginate_offset_async(
    fetch: Callable[[int, int], Awaitable[dict[str, Any]]],
    items_key: str,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> AsyncIterator[Any]:
    """Async variant of :func:`paginate_offset`."""
    offset = 0
    while True:
        page = await fetch(offset, page_size)
        items = page.get(items_key) or []
        for item in items:
            yield item
        if len(items) < page_size:
            return
        offset += page_size


async def paginate_cursor_async(
    fetch: Callable[[str | None], Awaitable[dict[str, Any]]],
    items_key: str,
) -> AsyncIterator[Any]:
    """Async variant of :func:`paginate_cursor`."""
    cursor: str | None = None
    while True:
        page = await fetch(cursor)
        items = page.get(items_key) or []
        for item in items:
            yield item
        if page.get("eof"):
            return
        cursor = page.get("nextCursor")
        if not cursor:
            return
