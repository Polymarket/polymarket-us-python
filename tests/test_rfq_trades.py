"""RFQ trade-history transport and live wire-contract regressions."""

import asyncio
import base64
import json
from unittest.mock import Mock

import pytest
from nacl.signing import SigningKey
from pytest_httpx import HTTPXMock
from websockets.asyncio.server import ServerConnection, serve

from polymarket_us import AsyncPolymarketUS, PolymarketUS
from polymarket_us.errors import (
    APIStatusError,
    AuthenticationError,
    BadRequestError,
    PermissionDeniedError,
)
from polymarket_us.types import GetRFQTradesParams, GetRFQTradesResponse
from polymarket_us.websocket import RFQEvent
from tests.types.rfq_trades import frames, params, trade

TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="


async def get_trades(
    asynchronous: bool,
    query: GetRFQTradesParams | None = None,
    *,
    authenticated: bool = True,
) -> GetRFQTradesResponse:
    key_id = "offline" if authenticated else None
    secret_key = TEST_SECRET_KEY if authenticated else None
    if asynchronous:
        async with AsyncPolymarketUS(
            key_id=key_id, secret_key=secret_key, api_base_url="https://api.test"
        ) as client:
            return (
                await client.rfqs.trades(query) if query is not None else await client.rfqs.trades()
            )
    with PolymarketUS(
        key_id=key_id, secret_key=secret_key, api_base_url="https://api.test"
    ) as client:
        return client.rfqs.trades(query) if query is not None else client.rfqs.trades()


@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
async def test_trade_history_filters_signature_and_precision(
    httpx_mock: HTTPXMock, asynchronous: bool
) -> None:
    response: GetRFQTradesResponse = {"trades": [trade], "cursor": "next+/="}
    httpx_mock.add_response(json=response)
    original_params = dict(params)

    assert await get_trades(asynchronous, params) == response
    assert params == original_params
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "GET"
    assert request.url.host == "api.test"
    assert request.url.path == "/v1/rfqs/trades"
    assert dict(request.url.params) == {key: str(value) for key, value in params.items()}
    assert request.content == b""
    assert request.headers["X-PM-Access-Key"] == "offline"
    timestamp = request.headers["X-PM-Timestamp"]
    message = f"{timestamp}GET/v1/rfqs/trades".encode()
    SigningKey(base64.b64decode(TEST_SECRET_KEY)).verify_key.verify(
        message, base64.b64decode(request.headers["X-PM-Signature"])
    )


@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("query", [None, {}], ids=["omitted", "empty"])
async def test_trade_history_without_filters(
    httpx_mock: HTTPXMock, asynchronous: bool, query: GetRFQTradesParams | None
) -> None:
    httpx_mock.add_response(json={"trades": [], "cursor": ""})
    assert await get_trades(asynchronous, query) == {"trades": [], "cursor": ""}
    assert str(httpx_mock.get_requests()[0].url) == "https://api.test/v1/rfqs/trades"


@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
async def test_empty_page_cursor_is_available_for_manual_continuation(
    httpx_mock: HTTPXMock, asynchronous: bool
) -> None:
    cursor = "opaque+/=continuation"
    httpx_mock.add_response(json={"trades": [], "cursor": cursor})
    httpx_mock.add_response(json={"trades": [trade], "cursor": ""})
    filters: GetRFQTradesParams = {"limit": 2, "symbol": "Combo-A"}

    first = await get_trades(asynchronous, filters)
    assert first == {"trades": [], "cursor": cursor}
    assert len(httpx_mock.get_requests()) == 1
    second = await get_trades(asynchronous, {**filters, "cursor": first["cursor"]})
    assert second == {"trades": [trade], "cursor": ""}
    assert dict(httpx_mock.get_requests()[1].url.params) == {
        "limit": "2",
        "symbol": "Combo-A",
        "cursor": cursor,
    }


@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
async def test_trade_history_requires_authentication(
    httpx_mock: HTTPXMock, asynchronous: bool
) -> None:
    with pytest.raises(AuthenticationError):
        await get_trades(asynchronous, authenticated=False)
    assert httpx_mock.get_requests() == []


@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize(
    "status,error_type", [(400, BadRequestError), (403, PermissionDeniedError)]
)
async def test_trade_history_preserves_api_errors(
    httpx_mock: HTTPXMock, asynchronous: bool, status: int, error_type: type[APIStatusError]
) -> None:
    body = {"message": "RFQ history unavailable"}
    httpx_mock.add_response(
        status_code=status, json=body, headers={"x-request-id": "rfq-history-request"}
    )
    with pytest.raises(error_type) as caught:
        await get_trades(asynchronous, params)
    assert caught.value.status_code == status
    assert caught.value.body == body
    assert caught.value.request_id == "rfq-history-request"
    assert len(httpx_mock.get_requests()) == 1


@pytest.mark.parametrize("frame", frames, ids=["trade", "null-timestamp", "null-trade"])
async def test_live_rfq_trade_reaches_callback(frame: RFQEvent) -> None:
    async def handler(peer: ServerConnection) -> None:
        assert json.loads(await peer.recv()) == {
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
                assert callback.call_args.args[0] is raw.call_args_list[0].args[0]
                errors.assert_not_called()
            finally:
                await asyncio.wait_for(ws.close(), 5)
