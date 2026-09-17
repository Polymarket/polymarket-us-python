"""Offline contracts for private order snapshot subscriptions."""

import json
from unittest.mock import AsyncMock, Mock

import pytest

from polymarket_us.errors import WebSocketError
from polymarket_us.websocket.private import PrivateWebSocket
from polymarket_us.websocket.types import OrderSnapshot

TERMINAL: OrderSnapshot = {
    "requestId": "snapshot-1",
    "subscriptionType": "SUBSCRIPTION_TYPE_ORDER_SNAPSHOT",
    "orderSubscriptionSnapshot": {"orders": [], "eof": True},
}


@pytest.fixture
def ws() -> PrivateWebSocket:
    # Synthetic key from the public SDK tests; no live connection is made.
    return PrivateWebSocket(
        key_id="offline", secret_key="nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="
    )


async def test_live_and_snapshot_subscriptions_use_distinct_types(ws: PrivateWebSocket) -> None:
    send = AsyncMock()
    ws.send = send
    await ws.subscribe_orders("live-1")
    await ws.subscribe("snapshot-1", "SUBSCRIPTION_TYPE_ORDER_SNAPSHOT")
    assert [call.args[0] for call in send.call_args_list] == [
        {"subscribe": {"requestId": "live-1", "subscriptionType": "SUBSCRIPTION_TYPE_ORDER"}},
        {
            "subscribe": {
                "requestId": "snapshot-1",
                "subscriptionType": "SUBSCRIPTION_TYPE_ORDER_SNAPSHOT",
            }
        },
    ]


@pytest.mark.parametrize("failed", [False, True])
def test_terminal_snapshot_dispatch(ws: PrivateWebSocket, failed: bool) -> None:
    snapshot = Mock()
    error = Mock()
    message = Mock()
    ws.on("order_snapshot", snapshot)
    ws.on("error", error)
    ws.on("message", message)
    frame = dict(TERMINAL)
    if failed:
        frame["error"] = "deadline exceeded"
    ws._handle_message(json.dumps(frame))
    message.assert_called_once_with(frame)
    if failed:
        snapshot.assert_not_called()
        error.assert_called_once()
        failure = error.call_args.args[0]
        assert isinstance(failure, WebSocketError)
        assert failure.request_id == "snapshot-1"
        assert str(failure) == "deadline exceeded"
    else:
        snapshot.assert_called_once_with(frame)
        error.assert_not_called()
