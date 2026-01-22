"""Tests for HTTP error handling."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from polymarket_us import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    PolymarketUS,
    RateLimitError,
)


class TestHTTPErrors:
    """Tests for HTTP error responses."""

    @pytest.fixture
    def client(self) -> PolymarketUS:
        """Create a client."""
        return PolymarketUS()

    def _make_mock_response(self, status_code: int, message: str, reason: str) -> MagicMock:
        """Create a mock response."""
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.is_success = False
        mock_response.status_code = status_code
        mock_response.text = f'{{"message": "{message}"}}'
        mock_response.json.return_value = {"message": message}
        mock_response.reason_phrase = reason
        mock_response.request = httpx.Request("GET", "http://test")
        return mock_response

    @patch.object(httpx.Client, "request")
    def test_400_raises_bad_request(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """400 should raise BadRequestError."""
        mock_request.return_value = self._make_mock_response(
            400, "Invalid parameters", "Bad Request"
        )

        with pytest.raises(BadRequestError) as exc_info:
            client.events.list()

        assert "Invalid parameters" in str(exc_info.value)
        assert exc_info.value.status_code == 400

    @patch.object(httpx.Client, "request")
    def test_401_raises_authentication_error(
        self, mock_request: MagicMock, client: PolymarketUS
    ) -> None:
        """401 should raise AuthenticationError."""
        mock_request.return_value = self._make_mock_response(401, "Invalid API key", "Unauthorized")

        with pytest.raises(AuthenticationError) as exc_info:
            client.events.list()

        assert exc_info.value.status_code == 401

    @patch.object(httpx.Client, "request")
    def test_403_raises_permission_denied(
        self, mock_request: MagicMock, client: PolymarketUS
    ) -> None:
        """403 should raise PermissionDeniedError."""
        mock_request.return_value = self._make_mock_response(403, "Forbidden", "Forbidden")

        with pytest.raises(PermissionDeniedError) as exc_info:
            client.events.list()

        assert exc_info.value.status_code == 403

    @patch.object(httpx.Client, "request")
    def test_404_raises_not_found(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """404 should raise NotFoundError."""
        mock_request.return_value = self._make_mock_response(404, "Event not found", "Not Found")

        with pytest.raises(NotFoundError) as exc_info:
            client.events.retrieve(99999)

        assert exc_info.value.status_code == 404

    @patch.object(httpx.Client, "request")
    def test_429_raises_rate_limit(self, mock_request: MagicMock, client: PolymarketUS) -> None:
        """429 should raise RateLimitError."""
        mock_request.return_value = self._make_mock_response(
            429, "Too many requests", "Too Many Requests"
        )

        with pytest.raises(RateLimitError) as exc_info:
            client.events.list()

        assert exc_info.value.status_code == 429

    @patch.object(httpx.Client, "request")
    def test_500_raises_internal_server_error(
        self, mock_request: MagicMock, client: PolymarketUS
    ) -> None:
        """500 should raise InternalServerError."""
        mock_request.return_value = self._make_mock_response(
            500, "Internal error", "Internal Server Error"
        )

        with pytest.raises(InternalServerError) as exc_info:
            client.events.list()

        assert exc_info.value.status_code == 500

    @patch.object(httpx.Client, "request")
    def test_502_raises_internal_server_error(
        self, mock_request: MagicMock, client: PolymarketUS
    ) -> None:
        """502 should raise InternalServerError."""
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.is_success = False
        mock_response.status_code = 502
        mock_response.text = ""
        mock_response.reason_phrase = "Bad Gateway"
        mock_response.request = httpx.Request("GET", "http://test")
        mock_request.return_value = mock_response

        with pytest.raises(InternalServerError) as exc_info:
            client.events.list()

        assert exc_info.value.status_code == 502

    @patch.object(httpx.Client, "request")
    def test_timeout_raises_timeout_error(
        self, mock_request: MagicMock, client: PolymarketUS
    ) -> None:
        """Timeout should raise APITimeoutError."""
        mock_request.side_effect = httpx.TimeoutException("Connection timed out")

        with pytest.raises(APITimeoutError):
            client.events.list()

    @patch.object(httpx.Client, "request")
    def test_connection_error_raises_connection_error(
        self, mock_request: MagicMock, client: PolymarketUS
    ) -> None:
        """Connection error should raise APIConnectionError."""
        mock_request.side_effect = httpx.ConnectError("Failed to connect")

        with pytest.raises(APIConnectionError):
            client.events.list()
