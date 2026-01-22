"""Tests for series endpoints."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from polymarket_us import PolymarketUS


class TestSeriesList:
    """Tests for series.list()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_list_series(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should list series."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"series": []}'
        mock_response.json.return_value = {
            "series": [{"id": 1, "name": "NBA Finals"}, {"id": 2, "name": "World Series"}]
        }
        mock_request.return_value = mock_response

        response = client.series.list()

        assert "series" in response
        mock_request.assert_called_once()

    @patch.object(httpx.Client, "request")
    def test_passes_query_params(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should pass query params."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"series": []}'
        mock_response.json.return_value = {"series": []}
        mock_request.return_value = mock_response

        client.series.list({"limit": 10})

        call_kwargs = mock_request.call_args.kwargs
        params = call_kwargs.get("params", [])
        param_dict = dict(params)
        assert param_dict.get("limit") == "10"

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"series": []}'
        mock_response.json.return_value = {"series": []}
        mock_request.return_value = mock_response

        client.series.list()

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/series" in url


class TestSeriesRetrieve:
    """Tests for series.retrieve()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_retrieve_series_by_id(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should retrieve series by ID."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"series": {}}'
        mock_response.json.return_value = {"series": {"id": 123, "name": "Test Series"}}
        mock_request.return_value = mock_response

        response = client.series.retrieve(123)

        assert "series" in response

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"series": {}}'
        mock_response.json.return_value = {"series": {}}
        mock_request.return_value = mock_response

        client.series.retrieve(456)

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/series/id/456" in url
