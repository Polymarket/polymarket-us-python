"""Tests for search endpoints."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from polymarket_us import PolymarketUS


class TestSearchQuery:
    """Tests for search.query()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_search_without_params(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should search without params."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"events": []}'
        mock_response.json.return_value = {"events": []}
        mock_request.return_value = mock_response

        response = client.search.query()

        assert "events" in response
        mock_request.assert_called_once()

    @patch.object(httpx.Client, "request")
    def test_passes_search_query_params(
        self, mock_request: MagicMock, client: PolymarketUS
    ) -> None:
        """Should pass search query params."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"events": []}'
        mock_response.json.return_value = {"events": []}
        mock_request.return_value = mock_response

        client.search.query({"query": "bitcoin", "limit": 5})

        call_kwargs = mock_request.call_args.kwargs
        params = call_kwargs.get("params", [])
        param_dict = dict(params)
        assert param_dict.get("query") == "bitcoin"
        assert param_dict.get("limit") == "5"

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"events": []}'
        mock_response.json.return_value = {"events": []}
        mock_request.return_value = mock_response

        client.search.query()

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/search" in url

    @patch.object(httpx.Client, "request")
    def test_calls_gateway_url(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should call gateway URL."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"events": []}'
        mock_response.json.return_value = {"events": []}
        mock_request.return_value = mock_response

        client.search.query()

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "gateway.polymarket.us" in url
