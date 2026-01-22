"""Tests for events endpoints."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from polymarket_us import PolymarketUS


class TestEventsList:
    """Tests for events.list()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_list_events(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should list events."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"events": [{"id": 1}, {"id": 2}]}'
        mock_response.json.return_value = {
            "events": [
                {"id": 1, "slug": "event-1", "title": "Event 1"},
                {"id": 2, "slug": "event-2", "title": "Event 2"},
            ]
        }
        mock_request.return_value = mock_response

        response = client.events.list()

        assert "events" in response
        assert len(response["events"]) == 2

    @patch.object(httpx.Client, "request")
    def test_passes_query_params(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should pass query params."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"events": []}'
        mock_response.json.return_value = {"events": []}
        mock_request.return_value = mock_response

        client.events.list({"limit": 10, "active": True})

        call_kwargs = mock_request.call_args.kwargs
        params = call_kwargs.get("params", [])
        param_dict = dict(params)
        assert param_dict.get("limit") == "10"
        assert param_dict.get("active") == "true"

    @patch.object(httpx.Client, "request")
    def test_calls_gateway_url(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should call gateway URL."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"events": []}'
        mock_response.json.return_value = {"events": []}
        mock_request.return_value = mock_response

        client.events.list()

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "gateway.polymarket.us" in url
        assert "/v1/events" in url


class TestEventsRetrieve:
    """Tests for events.retrieve()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_retrieve_event_by_id(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should retrieve event by ID."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"event": {"id": 123}}'
        mock_response.json.return_value = {"event": {"id": 123, "title": "Test Event"}}
        mock_request.return_value = mock_response

        response = client.events.retrieve(123)

        assert "event" in response
        assert response["event"]["id"] == 123

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"event": {}}'
        mock_response.json.return_value = {"event": {}}
        mock_request.return_value = mock_response

        client.events.retrieve(456)

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/events/456" in url


class TestEventsRetrieveBySlug:
    """Tests for events.retrieve_by_slug()."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_retrieve_event_by_slug(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should retrieve event by slug."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"event": {"slug": "super-bowl"}}'
        mock_response.json.return_value = {"event": {"slug": "super-bowl", "title": "Super Bowl"}}
        mock_request.return_value = mock_response

        response = client.events.retrieve_by_slug("super-bowl")

        assert "event" in response
        assert response["event"]["slug"] == "super-bowl"

    @patch.object(httpx.Client, "request")
    def test_uses_correct_path(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """Should use correct path."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.text = '{"event": {}}'
        mock_response.json.return_value = {"event": {}}
        mock_request.return_value = mock_response

        client.events.retrieve_by_slug("my-event")

        call_args = mock_request.call_args
        url = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("url")
        assert "/v1/events/slug/my-event" in url
