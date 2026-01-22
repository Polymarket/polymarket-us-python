"""Tests for orders endpoints."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from polymarket_us import AuthenticationError, PolymarketUS


class TestOrdersAuthenticationRequired:
    """Tests for authentication requirements."""

    def test_list_requires_auth(self) -> None:
        """Should throw AuthenticationError without credentials."""
        client = PolymarketUS()
        with pytest.raises(AuthenticationError):
            client.orders.list()

    def test_create_requires_auth(self) -> None:
        """Should throw AuthenticationError for create without credentials."""
        client = PolymarketUS()
        with pytest.raises(AuthenticationError):
            client.orders.create(
                {
                    "market_slug": "test",
                    "intent": "ORDER_INTENT_BUY_LONG",
                }
            )


class TestOrdersList:
    """Tests for orders.list()."""

    # 32-byte key, base64 encoded
    TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="

    @pytest.fixture
    def auth_client(self) -> PolymarketUS:
        """Create an authenticated client."""
        return PolymarketUS(
            key_id="test-key-id",
            secret_key=self.TEST_SECRET_KEY,
        )

    @patch.object(httpx.Client, "request")
    def test_list_open_orders(self, mock_request: MagicMock, auth_client: PolymarketUS) -> None:
        """Should list open orders with auth."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"orders": [{"id": "order-1"}, {"id": "order-2"}]}'
        mock_response.json.return_value = {"orders": [{"id": "order-1"}, {"id": "order-2"}]}
        mock_request.return_value = mock_response

        response = auth_client.orders.list()

        assert "orders" in response
        assert len(response["orders"]) == 2

    @patch.object(httpx.Client, "request")
    def test_includes_auth_headers(
        self, mock_request: MagicMock, auth_client: PolymarketUS
    ) -> None:
        """Should include auth headers."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"orders": []}'
        mock_response.json.return_value = {"orders": []}
        mock_request.return_value = mock_response

        auth_client.orders.list()

        call_kwargs = mock_request.call_args.kwargs
        headers = call_kwargs["headers"]
        assert "X-PM-Access-Key" in headers
        assert "X-PM-Timestamp" in headers
        assert "X-PM-Signature" in headers
        assert headers["X-PM-Access-Key"] == "test-key-id"

    @patch.object(httpx.Client, "request")
    def test_calls_api_url(self, mock_request: MagicMock, auth_client: PolymarketUS) -> None:
        """Should call API URL not gateway."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"orders": []}'
        mock_response.json.return_value = {"orders": []}
        mock_request.return_value = mock_response

        auth_client.orders.list()

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "api.polymarket.us" in url
        assert "/v1/orders/open" in url


class TestOrdersCreate:
    """Tests for orders.create()."""

    TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="

    @pytest.fixture
    def auth_client(self) -> PolymarketUS:
        """Create an authenticated client."""
        return PolymarketUS(
            key_id="test-key-id",
            secret_key=self.TEST_SECRET_KEY,
        )

    @patch.object(httpx.Client, "request")
    def test_create_order(self, mock_request: MagicMock, auth_client: PolymarketUS) -> None:
        """Should create order."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"id": "new-order-123"}'
        mock_response.json.return_value = {"id": "new-order-123"}
        mock_request.return_value = mock_response

        response = auth_client.orders.create(
            {
                "market_slug": "btc-100k",
                "intent": "ORDER_INTENT_BUY_LONG",
                "type": "ORDER_TYPE_LIMIT",
                "price": {"value": "0.55", "currency": "USD"},
                "quantity": 100,
            }
        )

        assert response["id"] == "new-order-123"

    @patch.object(httpx.Client, "request")
    def test_uses_post_method(self, mock_request: MagicMock, auth_client: PolymarketUS) -> None:
        """Should use POST method."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"id": "test"}'
        mock_response.json.return_value = {"id": "test"}
        mock_request.return_value = mock_response

        auth_client.orders.create(
            {
                "market_slug": "test",
                "intent": "ORDER_INTENT_BUY_LONG",
            }
        )

        call_args = mock_request.call_args
        method = call_args.args[0] if call_args.args else call_args.kwargs.get("method")
        assert method == "POST"


class TestOrdersRetrieve:
    """Tests for orders.retrieve()."""

    TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="

    @pytest.fixture
    def auth_client(self) -> PolymarketUS:
        """Create an authenticated client."""
        return PolymarketUS(
            key_id="test-key-id",
            secret_key=self.TEST_SECRET_KEY,
        )

    @patch.object(httpx.Client, "request")
    def test_retrieve_order_by_id(self, mock_request: MagicMock, auth_client: PolymarketUS) -> None:
        """Should retrieve order by ID."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"order": {"id": "order-123", "state": "ORDER_STATE_NEW"}}'
        mock_response.json.return_value = {"order": {"id": "order-123", "state": "ORDER_STATE_NEW"}}
        mock_request.return_value = mock_response

        response = auth_client.orders.retrieve("order-123")

        assert response["order"]["id"] == "order-123"

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, auth_client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"order": {}}'
        mock_response.json.return_value = {"order": {}}
        mock_request.return_value = mock_response

        auth_client.orders.retrieve("my-order-id")

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/order/my-order-id" in url


class TestOrdersCancelAll:
    """Tests for orders.cancel_all()."""

    TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="

    @pytest.fixture
    def auth_client(self) -> PolymarketUS:
        """Create an authenticated client."""
        return PolymarketUS(
            key_id="test-key-id",
            secret_key=self.TEST_SECRET_KEY,
        )

    @patch.object(httpx.Client, "request")
    def test_cancel_all_orders(self, mock_request: MagicMock, auth_client: PolymarketUS) -> None:
        """Should cancel all orders."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"canceledOrderIds": ["order-1", "order-2"]}'
        mock_response.json.return_value = {"canceledOrderIds": ["order-1", "order-2"]}
        mock_request.return_value = mock_response

        response = auth_client.orders.cancel_all()

        assert "canceledOrderIds" in response
        assert len(response["canceledOrderIds"]) == 2

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, auth_client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"canceledOrderIds": []}'
        mock_response.json.return_value = {"canceledOrderIds": []}
        mock_request.return_value = mock_response

        auth_client.orders.cancel_all()

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/orders/open/cancel" in url
