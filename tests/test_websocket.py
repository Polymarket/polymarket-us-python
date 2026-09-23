"""Tests for WebSocket functionality."""

import asyncio
import base64
from collections.abc import AsyncIterator
from typing import Literal

import pytest
from nacl.signing import SigningKey
from websockets.asyncio.server import ServerConnection, serve
from websockets.http11 import Request

from polymarket_us import AuthenticationError, PolymarketUS
from polymarket_us.errors import PolymarketUSError
from polymarket_us.websocket import MarketsWebSocket, PrivateWebSocket
from polymarket_us.websocket.base import BaseWebSocket

TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="


@pytest.mark.parametrize("stream", ["markets", "private"])
async def test_connect_sends_auth_headers(stream: Literal["markets", "private"]) -> None:
    requests: asyncio.Queue[Request] = asyncio.Queue()

    async def handler(connection: ServerConnection) -> None:
        assert connection.request is not None
        await requests.put(connection.request)
        await connection.send('{"heartbeat": {}}')
        await connection.wait_closed()

    async with serve(handler, "127.0.0.1", 0, close_timeout=1) as server:
        port = server.sockets[0].getsockname()[1]
        with PolymarketUS(
            key_id="test-key",
            secret_key=TEST_SECRET_KEY,
            api_base_url=f"http://127.0.0.1:{port}",
        ) as client:
            ws = client.ws.markets() if stream == "markets" else client.ws.private()
            heartbeat = asyncio.Event()
            ws.on("heartbeat", heartbeat.set)
            try:
                await asyncio.wait_for(ws.connect(), timeout=5)
                request = await asyncio.wait_for(requests.get(), timeout=5)
                assert request.path == f"/v1/ws/{stream}"
                assert request.headers["X-PM-Access-Key"] == "test-key"
                timestamp = request.headers["X-PM-Timestamp"]
                assert timestamp.isdigit()
                signature = base64.b64decode(request.headers["X-PM-Signature"])
                signing_key = SigningKey(base64.b64decode(TEST_SECRET_KEY))
                signing_key.verify_key.verify(
                    (timestamp + "GET" + request.path).encode(), signature
                )
                await asyncio.wait_for(heartbeat.wait(), timeout=5)
                assert ws.is_connected
            finally:
                await asyncio.wait_for(ws.close(), timeout=5)
            assert not ws.is_connected


@pytest.mark.parametrize("stream", ["markets", "private"])
class TestWebSocketLifecycle:
    @pytest.fixture
    async def connection(
        self, stream: Literal["markets", "private"]
    ) -> AsyncIterator[tuple[BaseWebSocket, ServerConnection]]:
        connections: asyncio.Queue[ServerConnection] = asyncio.Queue()

        async def handler(peer: ServerConnection) -> None:
            await connections.put(peer)
            await peer.wait_closed()

        async with serve(handler, "127.0.0.1", 0, close_timeout=1) as server:
            port = server.sockets[0].getsockname()[1]
            with PolymarketUS(
                key_id="test-key",
                secret_key=TEST_SECRET_KEY,
                api_base_url=f"http://127.0.0.1:{port}",
            ) as client:
                ws = client.ws.markets() if stream == "markets" else client.ws.private()
                try:
                    await asyncio.wait_for(ws.connect(), timeout=5)
                    peer = await asyncio.wait_for(connections.get(), timeout=5)
                    yield ws, peer
                finally:
                    await asyncio.wait_for(ws.close(), timeout=5)

    @pytest.mark.parametrize("close_code", [1000, 1001, 1011])
    async def test_remote_close_emits_once(
        self, connection: tuple[BaseWebSocket, ServerConnection], close_code: int
    ) -> None:
        ws, peer = connection
        events: list[str] = []
        errors: list[PolymarketUSError] = []
        heartbeat = asyncio.Event()
        ws.on("heartbeat", heartbeat.set)
        ws.on("close", lambda: events.append("close"))
        ws.once("close", lambda: events.append("once"))
        ws.on("error", errors.append)

        await asyncio.wait_for(peer.send('{"heartbeat": {}}'), timeout=5)
        await asyncio.wait_for(heartbeat.wait(), timeout=5)
        await asyncio.wait_for(peer.close(close_code), timeout=5)
        assert ws._message_task is not None
        await asyncio.wait_for(ws._message_task, timeout=5)

        assert not ws.is_connected
        assert events == ["close", "once"]
        assert errors == []
        await asyncio.wait_for(ws.close(), timeout=5)
        assert events == ["close", "once"]

    async def test_local_close_does_not_emit_close(
        self, connection: tuple[BaseWebSocket, ServerConnection]
    ) -> None:
        ws, peer = connection
        events: list[str] = []
        ws.on("close", lambda: events.append("close"))

        await asyncio.wait_for(ws.close(), timeout=5)
        await asyncio.wait_for(peer.wait_closed(), timeout=5)

        assert ws._message_task is not None
        assert ws._message_task.cancelled()
        assert not ws.is_connected
        assert events == []

    async def test_message_task_cancellation_does_not_emit_close(
        self, connection: tuple[BaseWebSocket, ServerConnection]
    ) -> None:
        ws, _ = connection
        events: list[str] = []
        ws.on("close", lambda: events.append("close"))
        assert ws._message_task is not None

        ws._message_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await asyncio.wait_for(ws._message_task, timeout=5)

        assert ws.is_connected
        assert events == []

    async def test_message_listener_error_does_not_emit_close(
        self, connection: tuple[BaseWebSocket, ServerConnection]
    ) -> None:
        ws, peer = connection
        events: list[str] = []
        errors: list[PolymarketUSError] = []

        def on_heartbeat() -> None:
            raise ValueError("listener failed")

        ws.on("heartbeat", on_heartbeat)
        ws.on("close", lambda: events.append("close"))
        ws.on("error", errors.append)
        await asyncio.wait_for(peer.send('{"heartbeat": {}}'), timeout=5)
        assert ws._message_task is not None
        await asyncio.wait_for(ws._message_task, timeout=5)

        assert ws.is_connected
        assert events == []
        assert len(errors) == 1
        assert isinstance(errors[0], PolymarketUSError)
        assert str(errors[0]) == "listener failed"


class TestWebSocketFactory:
    """Tests for WebSocket factory."""

    def test_has_ws_factory_on_client(self) -> None:
        """Should have ws factory on client."""
        client = PolymarketUS(key_id="test-key", secret_key=TEST_SECRET_KEY)
        assert client.ws is not None

    def test_creates_private_websocket_instance(self) -> None:
        """Should create private WebSocket instance."""
        client = PolymarketUS(key_id="test-key", secret_key=TEST_SECRET_KEY)
        private_ws = client.ws.private()
        assert isinstance(private_ws, PrivateWebSocket)

    def test_creates_markets_websocket_instance(self) -> None:
        """Should create markets WebSocket instance."""
        client = PolymarketUS(key_id="test-key", secret_key=TEST_SECRET_KEY)
        markets_ws = client.ws.markets()
        assert isinstance(markets_ws, MarketsWebSocket)

    def test_throws_without_credentials_for_private_websocket(self) -> None:
        """Should throw without credentials for private WebSocket."""
        client = PolymarketUS()
        with pytest.raises(AuthenticationError, match="credentials required"):
            client.ws.private()

    def test_throws_without_credentials_for_markets_websocket(self) -> None:
        """Should throw without credentials for markets WebSocket."""
        client = PolymarketUS()
        with pytest.raises(AuthenticationError, match="credentials required"):
            client.ws.markets()


class TestPrivateWebSocket:
    """Tests for PrivateWebSocket."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS(key_id="test-key", secret_key=TEST_SECRET_KEY)

    def test_has_connect_method(self, client: PolymarketUS) -> None:
        """Should have connect method."""
        ws = client.ws.private()
        assert hasattr(ws, "connect")
        assert callable(ws.connect)

    def test_has_close_method(self, client: PolymarketUS) -> None:
        """Should have close method."""
        ws = client.ws.private()
        assert hasattr(ws, "close")
        assert callable(ws.close)

    def test_has_subscribe_methods(self, client: PolymarketUS) -> None:
        """Should have subscribe methods."""
        ws = client.ws.private()
        assert hasattr(ws, "subscribe_orders")
        assert hasattr(ws, "subscribe_positions")
        assert hasattr(ws, "subscribe_account_balance")
        assert callable(ws.subscribe_orders)
        assert callable(ws.subscribe_positions)
        assert callable(ws.subscribe_account_balance)

    def test_has_unsubscribe_method(self, client: PolymarketUS) -> None:
        """Should have unsubscribe method."""
        ws = client.ws.private()
        assert hasattr(ws, "unsubscribe")
        assert callable(ws.unsubscribe)

    def test_has_on_method_for_event_listeners(self, client: PolymarketUS) -> None:
        """Should have on method for event listeners."""
        ws = client.ws.private()
        assert hasattr(ws, "on")
        assert callable(ws.on)

    def test_has_off_method_to_remove_listeners(self, client: PolymarketUS) -> None:
        """Should have off method to remove listeners."""
        ws = client.ws.private()
        assert hasattr(ws, "off")
        assert callable(ws.off)

    def test_has_is_connected_property(self, client: PolymarketUS) -> None:
        """Should have is_connected property."""
        ws = client.ws.private()
        assert hasattr(ws, "is_connected")
        assert ws.is_connected is False

    def test_accepts_event_listeners(self, client: PolymarketUS) -> None:
        """Should accept event listeners."""
        ws = client.ws.private()

        def on_order_snapshot(data: object) -> None:
            pass

        def on_order_update(data: object) -> None:
            pass

        def on_error(error: object) -> None:
            pass

        ws.on("order_snapshot", on_order_snapshot)
        ws.on("order_update", on_order_update)
        ws.on("error", on_error)


class TestMarketsWebSocket:
    """Tests for MarketsWebSocket."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS(key_id="test-key", secret_key=TEST_SECRET_KEY)

    def test_has_connect_method(self, client: PolymarketUS) -> None:
        """Should have connect method."""
        ws = client.ws.markets()
        assert hasattr(ws, "connect")
        assert callable(ws.connect)

    def test_has_close_method(self, client: PolymarketUS) -> None:
        """Should have close method."""
        ws = client.ws.markets()
        assert hasattr(ws, "close")
        assert callable(ws.close)

    def test_has_subscribe_methods(self, client: PolymarketUS) -> None:
        """Should have subscribe methods."""
        ws = client.ws.markets()
        assert hasattr(ws, "subscribe_market_data")
        assert hasattr(ws, "subscribe_market_data_lite")
        assert hasattr(ws, "subscribe_trades")
        assert callable(ws.subscribe_market_data)
        assert callable(ws.subscribe_market_data_lite)
        assert callable(ws.subscribe_trades)

    def test_has_unsubscribe_method(self, client: PolymarketUS) -> None:
        """Should have unsubscribe method."""
        ws = client.ws.markets()
        assert hasattr(ws, "unsubscribe")
        assert callable(ws.unsubscribe)

    def test_has_on_method_for_event_listeners(self, client: PolymarketUS) -> None:
        """Should have on method for event listeners."""
        ws = client.ws.markets()
        assert hasattr(ws, "on")
        assert callable(ws.on)

    def test_has_is_connected_property(self, client: PolymarketUS) -> None:
        """Should have is_connected property."""
        ws = client.ws.markets()
        assert hasattr(ws, "is_connected")
        assert ws.is_connected is False

    def test_accepts_event_listeners(self, client: PolymarketUS) -> None:
        """Should accept event listeners."""
        ws = client.ws.markets()

        def on_market_data(data: object) -> None:
            pass

        def on_trade(data: object) -> None:
            pass

        def on_error(error: object) -> None:
            pass

        ws.on("market_data", on_market_data)
        ws.on("trade", on_trade)
        ws.on("error", on_error)
