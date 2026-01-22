"""Tests for WebSocket functionality."""

import pytest

from polymarket_us import AuthenticationError, PolymarketUS
from polymarket_us.websocket import MarketsWebSocket, PrivateWebSocket

TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="


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
