"""Tests for sports endpoints."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from polymarket_us import PolymarketUS


class TestSportsList:
    """Tests for sports.list()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_list_sports(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should list sports."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"sports": []}'
        mock_response.json.return_value = {
            "sports": [
                {"id": "basketball", "name": "Basketball", "slug": "basketball"},
                {"id": "baseball", "name": "Baseball", "slug": "baseball"},
            ]
        }
        mock_request.return_value = mock_response

        response = client.sports.list()

        assert "sports" in response
        mock_request.assert_called_once()

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"sports": []}'
        mock_response.json.return_value = {"sports": []}
        mock_request.return_value = mock_response

        client.sports.list()

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/sports" in url


class TestSportsTeams:
    """Tests for sports.teams()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_list_teams(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should list teams."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"teams": {}}'
        mock_response.json.return_value = {
            "teams": {
                "lakers": {"id": 1, "name": "Lakers"},
                "celtics": {"id": 2, "name": "Celtics"},
            }
        }
        mock_request.return_value = mock_response

        response = client.sports.teams()

        assert "teams" in response

    @patch.object(httpx.Client, "request")
    def test_passes_query_params(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should pass query params."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"teams": {}}'
        mock_response.json.return_value = {"teams": {}}
        mock_request.return_value = mock_response

        client.sports.teams({"provider": "espn", "league": "nba"})

        call_kwargs = mock_request.call_args.kwargs
        params = call_kwargs.get("params", [])
        param_dict = dict(params)
        assert param_dict.get("provider") == "espn"
        assert param_dict.get("league") == "nba"

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"teams": {}}'
        mock_response.json.return_value = {"teams": {}}
        mock_request.return_value = mock_response

        client.sports.teams()

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/sports/teams/provider" in url
