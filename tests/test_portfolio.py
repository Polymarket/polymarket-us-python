"""Tests for portfolio and account endpoints."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from polymarket_us import AuthenticationError, PolymarketUS

TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="


class TestPortfolioPositions:
    """Tests for portfolio.positions()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @pytest.fixture
    def auth_client(self) -> PolymarketUS:
        return PolymarketUS(key_id="test-key-id", secret_key=TEST_SECRET_KEY)

    def test_requires_authentication(self, client: PolymarketUS) -> None:
        """Should require authentication."""
        with pytest.raises(AuthenticationError):
            client.portfolio.positions()

    @patch.object(httpx.Client, "request")
    def test_get_positions_with_auth(
        self, mock_request: MagicMock, auth_client: PolymarketUS
    ) -> None:
        """Should get positions with auth."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"positions": {}}'
        mock_response.json.return_value = {
            "positions": {
                "btc-100k": {"netPosition": "100", "cost": {"value": "55", "currency": "USD"}}
            }
        }
        mock_request.return_value = mock_response

        response = auth_client.portfolio.positions()

        assert "positions" in response
        assert "btc-100k" in response["positions"]

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, auth_client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"positions": {}}'
        mock_response.json.return_value = {"positions": {}}
        mock_request.return_value = mock_response

        auth_client.portfolio.positions()

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/portfolio/positions" in url


class TestPortfolioActivities:
    """Tests for portfolio.activities()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @pytest.fixture
    def auth_client(self) -> PolymarketUS:
        return PolymarketUS(key_id="test-key-id", secret_key=TEST_SECRET_KEY)

    def test_requires_authentication(self, client: PolymarketUS) -> None:
        """Should require authentication."""
        with pytest.raises(AuthenticationError):
            client.portfolio.activities()

    @patch.object(httpx.Client, "request")
    def test_get_activities_with_auth(
        self, mock_request: MagicMock, auth_client: PolymarketUS
    ) -> None:
        """Should get activities with auth."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"activities": []}'
        mock_response.json.return_value = {"activities": [{"type": "ACTIVITY_TYPE_TRADE"}]}
        mock_request.return_value = mock_response

        response = auth_client.portfolio.activities()

        assert "activities" in response
        assert len(response["activities"]) == 1

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, auth_client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"activities": []}'
        mock_response.json.return_value = {"activities": []}
        mock_request.return_value = mock_response

        auth_client.portfolio.activities()

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/portfolio/activities" in url


class TestAccountBalances:
    """Tests for account.balances()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @pytest.fixture
    def auth_client(self) -> PolymarketUS:
        return PolymarketUS(key_id="test-key-id", secret_key=TEST_SECRET_KEY)

    def test_requires_authentication(self, client: PolymarketUS) -> None:
        """Should require authentication."""
        with pytest.raises(AuthenticationError):
            client.account.balances()

    @patch.object(httpx.Client, "request")
    def test_get_balances_with_auth(
        self, mock_request: MagicMock, auth_client: PolymarketUS
    ) -> None:
        """Should get balances with auth."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"balances": []}'
        mock_response.json.return_value = {
            "balances": [{"currentBalance": 1000, "currency": "USD", "buyingPower": 800}]
        }
        mock_request.return_value = mock_response

        response = auth_client.account.balances()

        assert "balances" in response
        assert response["balances"][0]["currentBalance"] == 1000

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, auth_client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"balances": []}'
        mock_response.json.return_value = {"balances": []}
        mock_request.return_value = mock_response

        auth_client.account.balances()

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/account/balances" in url
