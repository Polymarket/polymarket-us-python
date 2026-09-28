"""RFQ wire regressions from gateway eb891a3e and protojson EmitUnpopulated."""

import asyncio
import json
from unittest.mock import Mock

import pytest
from websockets.asyncio.server import ServerConnection, serve

from polymarket_us import PolymarketUS
from polymarket_us.errors import WebSocketError
from polymarket_us.websocket import PrivateWebSocket, RFQEvent
from tests.types.rfq_callbacks import frames

TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="


@pytest.mark.parametrize(
    "frame", frames, ids=[next(iter(frame["rfqEvent"]), "emptyEvent") for frame in frames]
)
async def test_gateway_rfq_frames_reach_callback(frame: RFQEvent) -> None:
    async def handler(peer: ServerConnection) -> None:
        request = json.loads(await peer.recv())
        assert request == {
            "subscribe": {"requestId": "rfqs", "subscriptionType": "SUBSCRIPTION_TYPE_RFQ"}
        }
        await peer.send(json.dumps(frame))
        await peer.send('{"heartbeat": {}}')
        await peer.wait_closed()

    async with serve(handler, "127.0.0.1", 0, close_timeout=1) as server:
        port = server.sockets[0].getsockname()[1]
        with PolymarketUS(
            key_id="offline", secret_key=TEST_SECRET_KEY, api_base_url=f"http://127.0.0.1:{port}"
        ) as client:
            ws = client.ws.private()
            raw, callback, errors = Mock(), Mock(), Mock()
            done = asyncio.Event()
            ws.on("message", raw)
            ws.on("rfq_event", callback)
            ws.on("error", errors)
            ws.on("heartbeat", done.set)
            try:
                await asyncio.wait_for(ws.connect(), 5)
                await ws.subscribe_rfq("rfqs")
                await asyncio.wait_for(done.wait(), 5)
                callback.assert_called_once_with(frame)
                assert raw.call_count == 2
                assert callback.call_args.args[0] is raw.call_args_list[0].args[0]
                errors.assert_not_called()
            finally:
                await asyncio.wait_for(ws.close(), 5)


@pytest.mark.parametrize("error", ["", "subscription failed"])
def test_rfq_error_precedence(error: str) -> None:
    ws = PrivateWebSocket(key_id="offline", secret_key=TEST_SECRET_KEY)
    raw, callback, errors = Mock(), Mock(), Mock()
    ws.on("message", raw)
    ws.on("rfq_event", callback)
    ws.on("error", errors)
    frame = {**frames[0], "error": error}
    ws._handle_message(json.dumps(frame))
    raw.assert_called_once_with(frame)
    if error:
        callback.assert_not_called()
        errors.assert_called_once()
        failure = errors.call_args.args[0]
        assert isinstance(failure, WebSocketError)
        assert failure.request_id == "rfqs"
        assert str(failure) == error
    else:
        errors.assert_not_called()
        callback.assert_called_once_with(frame)
        assert callback.call_args.args[0] is raw.call_args.args[0]
