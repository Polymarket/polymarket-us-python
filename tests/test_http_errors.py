"""Tests for HTTP error handling."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from polymarket_us import (
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PolymarketUS,
    RateLimitError,
)


class TestHTTPErrors:
    """Tests for HTTP error handling."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        """Create a client."""
        return PolymarketUS()

    @patch.object(httpx.Client, "request")
    def test_400_raises_bad_request(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """400 should raise BadRequestError."""
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 400
        mock_response.text = '{"message": "Invalid parameters"}'
        mock_response.json.return_value = {"message": "Invalid parameters"}
        mock_response.reason_phrase = "Bad Request"
        mock_request.return_value = mock_response

        with pytest.raises(BadRequestError) as exc_info:
            client.events.list()

        assert "Invalid parameters" in str(exc_info.value)

    @patch.object(httpx.Client, "request")
    def test_401_raises_authentication_error(
        self, mock_request: MagicMock, client: PolymarketUS
    ) -> None:
        """401 should raise AuthenticationError."""
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 401
        mock_response.text = '{"message": "Invalid API key"}'
        mock_response.json.return_value = {"message": "Invalid API key"}
        mock_response.reason_phrase = "Unauthorized"
        mock_request.return_value = mock_response

        with pytest.raises(AuthenticationError):
            client.events.list()

    @patch.object(httpx.Client, "request")
    def test_404_raises_not_found(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """404 should raise NotFoundError."""
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 404
        mock_response.text = '{"message": "Event not found"}'
        mock_response.json.return_value = {"message": "Event not found"}
        mock_response.reason_phrase = "Not Found"
        mock_request.return_value = mock_response

        with pytest.raises(NotFoundError):
            client.events.retrieve(99999)

    @patch.object(httpx.Client, "request")
    def test_429_raises_rate_limit(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """429 should raise RateLimitError."""
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 429
        mock_response.text = '{"message": "Too many requests"}'
        mock_response.json.return_value = {"message": "Too many requests"}
        mock_response.reason_phrase = "Too Many Requests"
        mock_request.return_value = mock_response

        with pytest.raises(RateLimitError):
            client.events.list()

    @patch.object(httpx.Client, "request")
    def test_500_raises_internal_server_error(
        self, mock_request: MagicMock, client: PolymarketUS
    ) -> None:
        """500 should raise InternalServerError."""
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 500
        mock_response.text = '{"message": "Internal error"}'
        mock_response.json.return_value = {"message": "Internal error"}
        mock_response.reason_phrase = "Internal Server Error"
        mock_request.return_value = mock_response

        with pytest.raises(InternalServerError):
            client.events.list()

    @patch.object(httpx.Client, "request")
    def test_502_raises_internal_server_error(
        self, mock_request: MagicMock, client: PolymarketUS
    ) -> None:
        """502 should raise InternalServerError."""
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 502
        mock_response.text = ""
        mock_response.reason_phrase = "Bad Gateway"
        mock_request.return_value = mock_response

        with pytest.raises(InternalServerError):
            client.events.list()
