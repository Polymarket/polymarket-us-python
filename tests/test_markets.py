"""Tests for markets endpoints."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from polymarket_us import PolymarketUS


class TestMarketsList:
    """Tests for markets.list()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_list_markets(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should list markets."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"markets": [{"id": 1}, {"id": 2}]}'
        mock_response.json.return_value = {
            "markets": [{"id": 1, "slug": "market-1"}, {"id": 2, "slug": "market-2"}]
        }
        mock_request.return_value = mock_response

        response = client.markets.list()

        assert "markets" in response
        assert len(response["markets"]) == 2


class TestMarketsRetrieve:
    """Tests for markets.retrieve()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_retrieve_market_by_id(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should retrieve market by ID."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"market": {"id": 123}}'
        mock_response.json.return_value = {"market": {"id": 123, "slug": "btc-100k"}}
        mock_request.return_value = mock_response

        response = client.markets.retrieve(123)

        assert response["market"]["id"] == 123

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path_with_id(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should use correct path with id."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"market": {}}'
        mock_response.json.return_value = {"market": {}}
        mock_request.return_value = mock_response

        client.markets.retrieve(456)

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/market/id/456" in url


class TestMarketsRetrieveBySlug:
    """Tests for markets.retrieve_by_slug()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path_with_slug(
        self, mock_request: MagicMock, client: PolymarketUS
    ) -> None:
        """Should use correct path with slug."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"market": {}}'
        mock_response.json.return_value = {"market": {}}
        mock_request.return_value = mock_response

        client.markets.retrieve_by_slug("btc-100k")

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/market/slug/btc-100k" in url


class TestMarketsBook:
    """Tests for markets.book()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_get_order_book(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should get order book."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"marketSlug": "btc-100k", "bids": [], "offers": []}'
        mock_response.json.return_value = {
            "marketSlug": "btc-100k",
            "bids": [{"px": {"value": "0.55", "currency": "USD"}, "qty": "100"}],
            "offers": [{"px": {"value": "0.56", "currency": "USD"}, "qty": "80"}],
            "state": "MARKET_STATE_OPEN",
        }
        mock_request.return_value = mock_response

        book = client.markets.book("btc-100k")

        assert book["marketSlug"] == "btc-100k"
        assert "bids" in book
        assert "offers" in book

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"bids": [], "offers": []}'
        mock_response.json.return_value = {"bids": [], "offers": []}
        mock_request.return_value = mock_response

        client.markets.book("test-market")

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/markets/test-market/book" in url


class TestMarketsBBO:
    """Tests for markets.bbo()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_get_best_bid_offer(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should get best bid/offer."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"marketSlug": "btc-100k"}'
        mock_response.json.return_value = {
            "marketSlug": "btc-100k",
            "bestBid": {"value": "0.55", "currency": "USD"},
            "bestAsk": {"value": "0.56", "currency": "USD"},
        }
        mock_request.return_value = mock_response

        bbo = client.markets.bbo("btc-100k")

        assert "bestBid" in bbo
        assert "bestAsk" in bbo

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = "{}"
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        client.markets.bbo("test-market")

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/markets/test-market/bbo" in url


class TestMarketsSettlement:
    """Tests for markets.settlement()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = "{}"
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        client.markets.settlement("settled-market")

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/markets/settled-market/settlement" in url
