"""Tests for WebSocket auto-reconnect, resubscribe, and auth handling."""

from unittest.mock import AsyncMock, patch

import pytest

from polymarket_us import PolymarketUS
from polymarket_us.websocket.base import _upgrade_status

TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="


@pytest.fixture
def client() -> PolymarketUS:
    return PolymarketUS(key_id="test-key", secret_key=TEST_SECRET_KEY)


class TestSubscriptionTracking:
    """Subscriptions are recorded for replay and cleared on unsubscribe."""

    async def test_subscribe_records_subscription(self, client: PolymarketUS) -> None:
        ws = client.ws.private()
        ws._ws = AsyncMock()

        await ws.subscribe_orders("ord-1", ["mkt-a"])

        assert "ord-1" in ws._subscriptions
        assert ws._subscriptions["ord-1"].subscription_type == "SUBSCRIPTION_TYPE_ORDER"
        assert ws._subscriptions["ord-1"].market_slugs == ["mkt-a"]

    async def test_unsubscribe_clears_subscription(self, client: PolymarketUS) -> None:
        ws = client.ws.markets()
        ws._ws = AsyncMock()

        await ws.subscribe_market_data("md-1", ["mkt-a"])
        assert "md-1" in ws._subscriptions

        await ws.unsubscribe("md-1")
        assert "md-1" not in ws._subscriptions

    async def test_resubscribe_replays_all_subscriptions(self, client: PolymarketUS) -> None:
        ws = client.ws.markets()
        ws._ws = AsyncMock()

        await ws.subscribe_market_data("md-1", ["mkt-a"])
        await ws.subscribe_trades("tr-1", ["mkt-b"])
        ws._ws.send.reset_mock()

        await ws._resubscribe()

        assert ws._ws.send.call_count == 2


class TestReconnect:
    """Reconnect loop honors backoff, resubscribe, and fatal auth failures."""

    @patch("asyncio.sleep", new_callable=AsyncMock)
    async def test_reconnects_after_transient_failure(
        self, _sleep: AsyncMock, client: PolymarketUS
    ) -> None:
        ws = client.ws.private()
        ws._open_socket = AsyncMock(side_effect=[ConnectionError("dropped"), None])
        reconnected = []
        ws.on("reconnect", lambda: reconnected.append(True))

        result = await ws._reconnect()

        assert result is True
        assert ws._open_socket.call_count == 2
        assert reconnected == [True]

    @patch("asyncio.sleep", new_callable=AsyncMock)
    async def test_does_not_reconnect_on_auth_failure(
        self, _sleep: AsyncMock, client: PolymarketUS
    ) -> None:
        class _Resp:
            status_code = 401

        class _UpgradeError(Exception):
            response = _Resp()

        ws = client.ws.private()
        ws._open_socket = AsyncMock(side_effect=_UpgradeError())
        errors = []
        ws.on("error", lambda e: errors.append(e))

        result = await ws._reconnect()

        assert result is False
        assert len(errors) == 1

    @patch("asyncio.sleep", new_callable=AsyncMock)
    async def test_stops_reconnect_after_max_attempts(
        self, _sleep: AsyncMock, client: PolymarketUS
    ) -> None:
        ws = client.ws.private()
        ws.reconnect_max_attempts = 3
        ws._open_socket = AsyncMock(side_effect=ConnectionError("dropped"))

        result = await ws._reconnect()

        assert result is False
        assert ws._open_socket.call_count == 3


class TestUpgradeStatus:
    """The upgrade-status helper supports both websockets exception shapes."""

    def test_modern_response_shape(self) -> None:
        class _Resp:
            status_code = 429

        class _Err(Exception):
            response = _Resp()

        assert _upgrade_status(_Err()) == 429

    def test_legacy_status_code_shape(self) -> None:
        class _Err(Exception):
            status_code = 403

        assert _upgrade_status(_Err()) == 403

    def test_no_status(self) -> None:
        assert _upgrade_status(ConnectionError("network")) is None
