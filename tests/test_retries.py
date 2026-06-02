"""Tests for automatic retries, User-Agent, and correlation-id behavior."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from polymarket_us import (
    AsyncPolymarketUS,
    BadRequestError,
    InternalServerError,
    PolymarketUS,
)

TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="


def _response(status_code: int, payload: dict | None = None) -> httpx.Response:
    return httpx.Response(
        status_code,
        json=payload if payload is not None else {"message": "error"},
        request=httpx.Request("GET", "http://test"),
    )


class TestSyncRetries:
    """Retry behavior for the synchronous client."""

    @patch("time.sleep")
    @patch.object(httpx.Client, "request")
    def test_retries_get_on_500_then_succeeds(
        self, mock_request: MagicMock, mock_sleep: MagicMock
    ) -> None:
        mock_request.side_effect = [_response(500), _response(200, {"events": []})]
        client = PolymarketUS()

        result = client.events.list()

        assert result == {"events": []}
        assert mock_request.call_count == 2
        assert mock_sleep.call_count == 1

    @patch("time.sleep")
    @patch.object(httpx.Client, "request")
    def test_get_exhausts_retries(self, mock_request: MagicMock, mock_sleep: MagicMock) -> None:
        mock_request.return_value = _response(503)
        client = PolymarketUS(max_retries=2)

        with pytest.raises(InternalServerError):
            client.events.list()

        assert mock_request.call_count == 3  # initial + 2 retries
        assert mock_sleep.call_count == 2

    @patch("time.sleep")
    @patch.object(httpx.Client, "request")
    def test_retries_get_on_connect_error_then_succeeds(
        self, mock_request: MagicMock, mock_sleep: MagicMock
    ) -> None:
        mock_request.side_effect = [
            httpx.ConnectError("boom"),
            _response(200, {"events": []}),
        ]
        client = PolymarketUS()

        result = client.events.list()

        assert result == {"events": []}
        assert mock_request.call_count == 2
        assert mock_sleep.call_count == 1

    @patch("time.sleep")
    @patch.object(httpx.Client, "request")
    def test_post_is_never_retried(self, mock_request: MagicMock, mock_sleep: MagicMock) -> None:
        mock_request.return_value = _response(500)
        client = PolymarketUS(key_id="test-key", secret_key=TEST_SECRET_KEY)

        with pytest.raises(InternalServerError):
            client.orders.create({"marketSlug": "m", "intent": "ORDER_INTENT_BUY_LONG"})

        assert mock_request.call_count == 1
        assert mock_sleep.call_count == 0

    @patch.object(httpx.Client, "request")
    def test_4xx_is_not_retried(self, mock_request: MagicMock) -> None:
        mock_request.return_value = _response(400)
        client = PolymarketUS()

        with pytest.raises(BadRequestError):
            client.events.list()

        assert mock_request.call_count == 1

    @patch.object(httpx.Client, "request")
    def test_error_carries_request_id(self, mock_request: MagicMock) -> None:
        mock_request.return_value = _response(400)
        client = PolymarketUS(max_retries=0)

        with pytest.raises(BadRequestError) as exc_info:
            client.events.list()

        assert exc_info.value.request_id is not None

    @patch.object(httpx.Client, "request")
    def test_sends_user_agent_and_correlation_headers(self, mock_request: MagicMock) -> None:
        mock_request.return_value = _response(200, {"events": []})
        client = PolymarketUS()

        client.events.list()

        headers = mock_request.call_args.kwargs["headers"]
        assert headers["User-Agent"].startswith("polymarket-us-python/")
        assert headers["poly-correlation-id"]


class TestAsyncRetries:
    """Retry behavior for the asynchronous client."""

    @patch("asyncio.sleep", new_callable=AsyncMock)
    @patch.object(httpx.AsyncClient, "request", new_callable=AsyncMock)
    async def test_async_retries_get_on_500_then_succeeds(
        self, mock_request: AsyncMock, mock_sleep: AsyncMock
    ) -> None:
        mock_request.side_effect = [_response(500), _response(200, {"events": []})]
        client = AsyncPolymarketUS()

        result = await client.events.list()

        assert result == {"events": []}
        assert mock_request.call_count == 2
        assert mock_sleep.await_count == 1
        await client.close()
