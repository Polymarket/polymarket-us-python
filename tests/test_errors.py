"""Tests for error classes."""

import httpx

from polymarket_us import (
    APIConnectionError,
    APIError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    PolymarketUSError,
    RateLimitError,
    WebSocketError,
)


def _make_response(status_code: int) -> httpx.Response:
    """Create a mock response."""
    return httpx.Response(status_code=status_code, request=httpx.Request("GET", "http://test"))


class TestPolymarketUSError:
    """Tests for PolymarketUSError."""

    def test_is_exception(self) -> None:
        """Should be an Exception."""
        error = PolymarketUSError("test")
        assert isinstance(error, Exception)

    def test_stores_message(self) -> None:
        """Should store message."""
        error = PolymarketUSError("test message")
        assert str(error) == "test message"


class TestAPIError:
    """Tests for APIError."""

    def test_stores_message(self) -> None:
        """Should store message."""
        error = APIError("test error")
        assert error.message == "test error"

    def test_stores_body(self) -> None:
        """Should store body."""
        error = APIError("error", body={"code": "test"})
        assert error.body == {"code": "test"}

    def test_is_polymarket_error(self) -> None:
        """Should be a PolymarketUSError."""
        error = APIError("error")
        assert isinstance(error, PolymarketUSError)


class TestAPIConnectionError:
    """Tests for APIConnectionError."""

    def test_default_message(self) -> None:
        """Should have default message."""
        error = APIConnectionError()
        assert "Connection error" in error.message

    def test_is_api_error(self) -> None:
        """Should be an APIError."""
        error = APIConnectionError()
        assert isinstance(error, APIError)


class TestAPITimeoutError:
    """Tests for APITimeoutError."""

    def test_message(self) -> None:
        """Should have timeout message."""
        error = APITimeoutError()
        assert "timed out" in error.message

    def test_is_connection_error(self) -> None:
        """Should be an APIConnectionError."""
        error = APITimeoutError()
        assert isinstance(error, APIConnectionError)


class TestAPIStatusError:
    """Tests for APIStatusError."""

    def test_stores_status_code(self) -> None:
        """Should store status code."""
        response = _make_response(500)
        error = APIStatusError("error", response=response)
        assert error.status_code == 500

    def test_stores_response(self) -> None:
        """Should store response."""
        response = _make_response(500)
        error = APIStatusError("error", response=response)
        assert error.response is response


class TestBadRequestError:
    """Tests for BadRequestError."""

    def test_is_status_error(self) -> None:
        """Should be an APIStatusError."""
        response = _make_response(400)
        error = BadRequestError("bad request", response=response)
        assert isinstance(error, APIStatusError)
        assert error.status_code == 400


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_is_status_error(self) -> None:
        """Should be an APIStatusError."""
        response = _make_response(401)
        error = AuthenticationError("auth failed", response=response)
        assert isinstance(error, APIStatusError)
        assert error.status_code == 401


class TestPermissionDeniedError:
    """Tests for PermissionDeniedError."""

    def test_is_status_error(self) -> None:
        """Should be an APIStatusError."""
        response = _make_response(403)
        error = PermissionDeniedError("forbidden", response=response)
        assert isinstance(error, APIStatusError)
        assert error.status_code == 403


class TestNotFoundError:
    """Tests for NotFoundError."""

    def test_is_status_error(self) -> None:
        """Should be an APIStatusError."""
        response = _make_response(404)
        error = NotFoundError("not found", response=response)
        assert isinstance(error, APIStatusError)
        assert error.status_code == 404


class TestRateLimitError:
    """Tests for RateLimitError."""

    def test_is_status_error(self) -> None:
        """Should be an APIStatusError."""
        response = _make_response(429)
        error = RateLimitError("rate limited", response=response)
        assert isinstance(error, APIStatusError)
        assert error.status_code == 429


class TestInternalServerError:
    """Tests for InternalServerError."""

    def test_is_status_error(self) -> None:
        """Should be an APIStatusError."""
        response = _make_response(500)
        error = InternalServerError("server error", response=response)
        assert isinstance(error, APIStatusError)
        assert error.status_code == 500


class TestWebSocketError:
    """Tests for WebSocketError."""

    def test_is_polymarket_error(self) -> None:
        """Should be a PolymarketUSError."""
        error = WebSocketError("test")
        assert isinstance(error, PolymarketUSError)

    def test_stores_request_id(self) -> None:
        """Should store request_id."""
        error = WebSocketError("test", request_id="req-123")
        assert error.request_id == "req-123"
