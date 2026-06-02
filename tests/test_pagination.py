"""Tests for auto-pagination iterators (offset and cursor)."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx

from polymarket_us import AsyncPolymarketUS, PolymarketUS

TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="


def _json(payload: dict) -> httpx.Response:
    return httpx.Response(200, json=payload, request=httpx.Request("GET", "http://test"))


class TestOffsetPagination:
    """Offset-based iterators (events, markets, series)."""

    @patch.object(httpx.Client, "request")
    def test_iterates_until_short_page(self, mock_request: MagicMock) -> None:
        mock_request.side_effect = [
            _json({"events": [{"id": 1}, {"id": 2}]}),
            _json({"events": [{"id": 3}]}),
        ]
        client = PolymarketUS()

        events = list(client.events.iterate(page_size=2))

        assert [e["id"] for e in events] == [1, 2, 3]
        assert mock_request.call_count == 2

    @patch.object(httpx.Client, "request")
    def test_stops_on_empty_page(self, mock_request: MagicMock) -> None:
        mock_request.side_effect = [
            _json({"markets": [{"id": 1}, {"id": 2}]}),
            _json({"markets": []}),
        ]
        client = PolymarketUS()

        markets = list(client.markets.iterate(page_size=2))

        assert [m["id"] for m in markets] == [1, 2]
        assert mock_request.call_count == 2

    @patch.object(httpx.Client, "request")
    def test_non_positive_page_size_terminates(self, mock_request: MagicMock) -> None:
        # page_size <= 0 must be clamped so the loop cannot spin forever.
        mock_request.side_effect = [
            _json({"events": [{"id": 1}]}),
            _json({"events": []}),
        ]
        client = PolymarketUS()

        events = list(client.events.iterate(page_size=0))

        assert [e["id"] for e in events] == [1]
        assert mock_request.call_count == 2

    @patch.object(httpx.Client, "request")
    def test_single_short_page_stops_immediately(self, mock_request: MagicMock) -> None:
        mock_request.side_effect = [_json({"series": [{"id": 1}]})]
        client = PolymarketUS()

        series = list(client.series.iterate(page_size=2))

        assert [s["id"] for s in series] == [1]
        assert mock_request.call_count == 1


class TestCursorPagination:
    """Cursor-based iterator (activities)."""

    @patch.object(httpx.Client, "request")
    def test_follows_cursor_until_eof(self, mock_request: MagicMock) -> None:
        mock_request.side_effect = [
            _json({"activities": [{"type": "a"}], "nextCursor": "c1", "eof": False}),
            _json({"activities": [{"type": "b"}], "eof": True}),
        ]
        client = PolymarketUS(key_id="k", secret_key=TEST_SECRET_KEY)

        activities = list(client.portfolio.iterate_activities())

        assert [a["type"] for a in activities] == ["a", "b"]
        assert mock_request.call_count == 2

    @patch.object(httpx.Client, "request")
    def test_stops_when_no_next_cursor(self, mock_request: MagicMock) -> None:
        mock_request.side_effect = [
            _json({"activities": [{"type": "a"}], "nextCursor": "", "eof": False}),
        ]
        client = PolymarketUS(key_id="k", secret_key=TEST_SECRET_KEY)

        activities = list(client.portfolio.iterate_activities())

        assert [a["type"] for a in activities] == ["a"]
        assert mock_request.call_count == 1


class TestAsyncPagination:
    """Async iterators mirror the sync behavior."""

    @patch.object(httpx.AsyncClient, "request", new_callable=AsyncMock)
    async def test_async_offset_iterate(self, mock_request: AsyncMock) -> None:
        mock_request.side_effect = [
            _json({"events": [{"id": 1}, {"id": 2}]}),
            _json({"events": [{"id": 3}]}),
        ]
        client = AsyncPolymarketUS()

        events = [e async for e in client.events.iterate(page_size=2)]

        assert [e["id"] for e in events] == [1, 2, 3]
        await client.close()

    @patch.object(httpx.AsyncClient, "request", new_callable=AsyncMock)
    async def test_async_cursor_iterate(self, mock_request: AsyncMock) -> None:
        mock_request.side_effect = [
            _json({"activities": [{"type": "a"}], "nextCursor": "c1", "eof": False}),
            _json({"activities": [{"type": "b"}], "eof": True}),
        ]
        client = AsyncPolymarketUS(key_id="k", secret_key=TEST_SECRET_KEY)

        activities = [a async for a in client.portfolio.iterate_activities()]

        assert [a["type"] for a in activities] == ["a", "b"]
        await client.close()
