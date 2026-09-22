"""Tests for markets endpoints."""

from unittest.mock import MagicMock, patch

import httpx
import pytest
from pytest_httpx import HTTPXMock

from polymarket_us import AsyncPolymarketUS, PolymarketUS
from polymarket_us.types import GetMarketBBOResponse, GetMarketBookResponse, MarketSettlement


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


@pytest.fixture(params=[False, True], ids=["populated", "empty"])
def book_response(request: pytest.FixtureRequest) -> GetMarketBookResponse:
    if request.param:
        return {
            "marketData": {
                "marketSlug": "btc-100k",
                "bids": [],
                "offers": [],
                "state": "MARKET_STATE_CLOSED",
                "stats": None,
                "transactTime": None,
            }
        }
    return {
        "marketData": {
            "marketSlug": "btc-100k",
            "bids": [{"px": {"value": "0.55", "currency": "USD"}, "qty": "100"}],
            "offers": [{"px": {"value": "0.56", "currency": "USD"}, "qty": "80"}],
            "state": "MARKET_STATE_OPEN",
            "stats": {"lastTradePx": {"value": "0.55", "currency": "USD"}},
            "transactTime": "2026-09-21T12:00:00Z",
        }
    }


@pytest.fixture(params=[False, True], ids=["populated", "empty"])
def bbo_response(request: pytest.FixtureRequest) -> GetMarketBBOResponse:
    if request.param:
        return {
            "marketData": {
                "marketSlug": "btc-100k",
                "bestBid": None,
                "bestAsk": None,
                "lastTradePx": None,
                "bidDepth": 0,
                "askDepth": 0,
                "sharesTraded": "",
                "openInterest": "",
            }
        }
    return {
        "marketData": {
            "marketSlug": "btc-100k",
            "bestBid": {"value": "0.55", "currency": "USD"},
            "bestAsk": {"value": "0.56", "currency": "USD"},
            "lastTradePx": {"value": "0.55", "currency": "USD"},
            "bidDepth": 1,
            "askDepth": 1,
            "sharesTraded": "100",
            "openInterest": "80",
        }
    }


def test_book_returns_wire_response(
    httpx_mock: HTTPXMock, book_response: GetMarketBookResponse
) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://gateway.polymarket.us/v1/markets/btc-100k/book",
        json=book_response,
    )
    with PolymarketUS() as client:
        assert client.markets.book("btc-100k") == book_response


async def test_async_book_returns_wire_response(
    httpx_mock: HTTPXMock, book_response: GetMarketBookResponse
) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://gateway.polymarket.us/v1/markets/btc-100k/book",
        json=book_response,
    )
    async with AsyncPolymarketUS() as client:
        assert await client.markets.book("btc-100k") == book_response


def test_bbo_returns_wire_response(
    httpx_mock: HTTPXMock, bbo_response: GetMarketBBOResponse
) -> None:
    httpx_mock.add_response(
        method="GET", url="https://gateway.polymarket.us/v1/markets/btc-100k/bbo", json=bbo_response
    )
    with PolymarketUS() as client:
        assert client.markets.bbo("btc-100k") == bbo_response


async def test_async_bbo_returns_wire_response(
    httpx_mock: HTTPXMock, bbo_response: GetMarketBBOResponse
) -> None:
    httpx_mock.add_response(
        method="GET", url="https://gateway.polymarket.us/v1/markets/btc-100k/bbo", json=bbo_response
    )
    async with AsyncPolymarketUS() as client:
        assert await client.markets.bbo("btc-100k") == bbo_response


@pytest.mark.parametrize("settlement", [0, 0.5, 1])
def test_settlement_returns_numeric_price(httpx_mock: HTTPXMock, settlement: float) -> None:
    response: MarketSettlement = {"slug": "btc-100k", "settlement": settlement}
    httpx_mock.add_response(
        method="GET",
        url="https://gateway.polymarket.us/v1/markets/btc-100k/settlement",
        json=response,
    )
    with PolymarketUS() as client:
        assert client.markets.settlement("btc-100k") == response


@pytest.mark.parametrize("settlement", [0, 0.5, 1])
async def test_async_settlement_returns_numeric_price(
    httpx_mock: HTTPXMock, settlement: float
) -> None:
    response: MarketSettlement = {"slug": "btc-100k", "settlement": settlement}
    httpx_mock.add_response(
        method="GET",
        url="https://gateway.polymarket.us/v1/markets/btc-100k/settlement",
        json=response,
    )
    async with AsyncPolymarketUS() as client:
        assert await client.markets.settlement("btc-100k") == response
