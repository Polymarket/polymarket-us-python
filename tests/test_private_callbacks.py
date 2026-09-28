"""Private stream wire contracts from gateway users.proto at 7d195963.

The JSON fixtures use the gateway's protojson EmitUnpopulated option and contain
only synthetic values. Socket tests exercise the public client and subscriptions.
"""

import asyncio
import copy
import json
from pathlib import Path
from unittest.mock import Mock

import pytest
from websockets.asyncio.server import ServerConnection, serve

from polymarket_us import PolymarketUS
from polymarket_us.errors import WebSocketError
from polymarket_us.websocket import PrivateWebSocket

FRAMES = json.loads(
    (Path(__file__).parent / "fixtures" / "private_position_balance.json").read_text()
)
TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="


@pytest.mark.parametrize(
    ("frame_index", "event"),
    [(0, "position_update"), (1, "account_balance_update"), (2, "account_balance_snapshot")],
)
@pytest.mark.parametrize("missing", ["neither", "before", "after"])
async def test_gateway_frames_reach_callbacks(frame_index: int, event: str, missing: str) -> None:
    frame = copy.deepcopy(FRAMES[frame_index])
    if missing != "neither":
        if frame_index == 0:
            frame["positionSubscription"][f"{missing}Position"] = None
        elif frame_index == 1:
            frame["accountBalancesUpdate"]["balanceChange"][f"{missing}Balance"] = None
        else:
            frame["accountBalancesSnapshot"]["balances"] = []

    async def handler(peer: ServerConnection) -> None:
        request = json.loads(await peer.recv())
        assert request == {
            "subscribe": {
                "requestId": frame["requestId"],
                "subscriptionType": frame["subscriptionType"],
            }
        }
        await peer.send(json.dumps(frame))
        # Receipt of the next heartbeat proves this data frame was dispatched.
        await peer.send('{"heartbeat": {}}')
        await peer.wait_closed()

    async with serve(handler, "127.0.0.1", 0, close_timeout=1) as server:
        port = server.sockets[0].getsockname()[1]
        with PolymarketUS(
            key_id="offline", secret_key=TEST_SECRET_KEY, api_base_url=f"http://127.0.0.1:{port}"
        ) as client:
            ws = client.ws.private()
            raw, callback, errors, snapshots = Mock(), Mock(), Mock(), Mock()
            done = asyncio.Event()
            ws.on("message", raw)
            ws.on(event, callback)
            ws.on("position_snapshot", snapshots)
            ws.on("error", errors)
            ws.on("heartbeat", done.set)
            try:
                await asyncio.wait_for(ws.connect(), 5)
                if frame_index == 0:
                    await ws.subscribe_positions(frame["requestId"])
                else:
                    await ws.subscribe_account_balance(frame["requestId"])
                await asyncio.wait_for(done.wait(), 5)
                callback.assert_called_once_with(frame)
                assert raw.call_count == 2
                assert callback.call_args.args[0] is raw.call_args_list[0].args[0]
                snapshots.assert_not_called()
                errors.assert_not_called()
            finally:
                await asyncio.wait_for(ws.close(), 5)


@pytest.mark.parametrize(
    ("key", "event"),
    [
        ("orderSubscriptionSnapshot", "order_snapshot"),
        ("ordersSnapshot", "order_snapshot"),
        ("orderSubscriptionUpdate", "order_update"),
        ("orderUpdate", "order_update"),
        ("positionSubscriptionSnapshot", "position_snapshot"),
        ("positionsSnapshot", "position_snapshot"),
        ("positionSubscriptionUpdate", "position_update"),
        ("positionUpdate", "position_update"),
        ("accountBalanceSubscriptionSnapshot", "account_balance_snapshot"),
        ("accountBalancesSnapshot", "account_balance_snapshot"),
        ("accountBalanceSubscriptionUpdate", "account_balance_update"),
        ("accountBalanceUpdate", "account_balance_update"),
    ],
)
def test_existing_aliases_preserve_raw_payload(key: str, event: str) -> None:
    ws = PrivateWebSocket(key_id="offline", secret_key=TEST_SECRET_KEY)
    raw, callback = Mock(), Mock()
    ws.on("message", raw)
    ws.on(event, callback)
    frame = {"requestId": "legacy", key: {"preserved": "value"}}
    ws._handle_message(json.dumps(frame))
    raw.assert_called_once_with(frame)
    callback.assert_called_once_with(frame)
    assert callback.call_args.args[0] is raw.call_args.args[0]


@pytest.mark.parametrize(
    ("frame_index", "event"),
    [(0, "position_update"), (1, "account_balance_update"), (2, "account_balance_snapshot")],
)
@pytest.mark.parametrize("error", ["", "subscription failed"])
def test_error_controls_data_dispatch(frame_index: int, event: str, error: str) -> None:
    ws = PrivateWebSocket(key_id="offline", secret_key=TEST_SECRET_KEY)
    raw, callback, errors = Mock(), Mock(), Mock()
    ws.on("message", raw)
    ws.on(event, callback)
    ws.on("error", errors)
    frame = {**FRAMES[frame_index], "error": error}
    ws._handle_message(json.dumps(frame))
    raw.assert_called_once_with(frame)
    if error:
        callback.assert_not_called()
        errors.assert_called_once()
        failure = errors.call_args.args[0]
        assert isinstance(failure, WebSocketError)
        assert failure.request_id == frame["requestId"]
        assert str(failure) == error
    else:
        errors.assert_not_called()
        callback.assert_called_once_with(frame)
        assert callback.call_args.args[0] is raw.call_args.args[0]
