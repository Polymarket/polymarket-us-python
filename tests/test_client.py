"""Tests for the PolymarketUS client."""

import pytest

from polymarket_us import PolymarketUS


class TestClientInitialization:
    """Tests for client initialization."""

    def test_create_client_without_options(self) -> None:
        """Should create client without any options."""
        client = PolymarketUS()
        assert client is not None

    def test_create_client_with_credentials(self) -> None:
        """Should create client with credentials."""
        client = PolymarketUS(
            key_id="test-key-id",
            secret_key="dGVzdC1zZWNyZXQta2V5MDEyMzQ1Njc4OTAxMjM0NQ==",
        )
        assert client is not None
        assert client.key_id == "test-key-id"

    def test_create_client_with_custom_base_urls(self) -> None:
        """Should create client with custom base URLs."""
        client = PolymarketUS(
            gateway_base_url="https://custom-gateway.example.com",
            api_base_url="https://custom-api.example.com",
        )
        assert client.gateway_base_url == "https://custom-gateway.example.com"
        assert client.api_base_url == "https://custom-api.example.com"

    def test_default_base_urls(self) -> None:
        """Should have default base URLs."""
        client = PolymarketUS()
        assert client.gateway_base_url == "https://gateway.polymarket.us"
        assert client.api_base_url == "https://api.polymarket.us"

    def test_default_timeout(self) -> None:
        """Should have default timeout."""
        client = PolymarketUS()
        assert client.timeout == 30.0

    def test_custom_timeout(self) -> None:
        """Should allow custom timeout."""
        client = PolymarketUS(timeout=60.0)
        assert client.timeout == 60.0


class TestResourceAccessors:
    """Tests for resource accessors."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        """Create a client for testing."""
        return PolymarketUS()

    def test_has_events_resource(self, client: PolymarketUS) -> None:
        """Should have events resource."""
        assert client.events is not None
        assert callable(client.events.list)
        assert callable(client.events.retrieve)
        assert callable(client.events.retrieve_by_slug)

    def test_has_markets_resource(self, client: PolymarketUS) -> None:
        """Should have markets resource."""
        assert client.markets is not None
        assert callable(client.markets.list)
        assert callable(client.markets.retrieve)
        assert callable(client.markets.retrieve_by_slug)
        assert callable(client.markets.book)
        assert callable(client.markets.bbo)
        assert callable(client.markets.settlement)

    def test_has_orders_resource(self, client: PolymarketUS) -> None:
        """Should have orders resource."""
        assert client.orders is not None
        assert callable(client.orders.create)
        assert callable(client.orders.list)
        assert callable(client.orders.retrieve)
        assert callable(client.orders.cancel)
        assert callable(client.orders.modify)
        assert callable(client.orders.cancel_all)
        assert callable(client.orders.preview)
        assert callable(client.orders.close_position)

    def test_has_portfolio_resource(self, client: PolymarketUS) -> None:
        """Should have portfolio resource."""
        assert client.portfolio is not None
        assert callable(client.portfolio.positions)
        assert callable(client.portfolio.activities)

    def test_has_account_resource(self, client: PolymarketUS) -> None:
        """Should have account resource."""
        assert client.account is not None
        assert callable(client.account.balances)

    def test_has_series_resource(self, client: PolymarketUS) -> None:
        """Should have series resource."""
        assert client.series is not None
        assert callable(client.series.list)
        assert callable(client.series.retrieve)

    def test_has_sports_resource(self, client: PolymarketUS) -> None:
        """Should have sports resource."""
        assert client.sports is not None
        assert callable(client.sports.list)
        assert callable(client.sports.teams)

    def test_has_search_resource(self, client: PolymarketUS) -> None:
        """Should have search resource."""
        assert client.search is not None
        assert callable(client.search.query)

    def test_has_ws_factory(self, client: PolymarketUS) -> None:
        """Should have WebSocket factory."""
        assert client.ws is not None
