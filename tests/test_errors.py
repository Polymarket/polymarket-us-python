"""Tests for error classes."""

from polymarket_us import (
    APIError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PolymarketUSError,
    RateLimitError,
    WebSocketError,
)


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

    def test_stores_status(self) -> None:
        """Should store status code."""
        error = APIError(500, "error")
        assert error.status == 500

    def test_stores_code(self) -> None:
        """Should store error code."""
        error = APIError(400, "error", "bad_request")
        assert error.code == "bad_request"

    def test_is_polymarket_error(self) -> None:
        """Should be a PolymarketUSError."""
        error = APIError(500, "error")
        assert isinstance(error, PolymarketUSError)


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_default_message(self) -> None:
        """Should have default message."""
        error = AuthenticationError()
        assert "Authentication failed" in str(error)

    def test_status_is_401(self) -> None:
        """Should have 401 status."""
        error = AuthenticationError()
        assert error.status == 401

    def test_code_is_authentication_error(self) -> None:
        """Should have authentication_error code."""
        error = AuthenticationError()
        assert error.code == "authentication_error"


class TestBadRequestError:
    """Tests for BadRequestError."""

    def test_status_is_400(self) -> None:
        """Should have 400 status."""
        error = BadRequestError()
        assert error.status == 400


class TestNotFoundError:
    """Tests for NotFoundError."""

    def test_status_is_404(self) -> None:
        """Should have 404 status."""
        error = NotFoundError()
        assert error.status == 404


class TestRateLimitError:
    """Tests for RateLimitError."""

    def test_status_is_429(self) -> None:
        """Should have 429 status."""
        error = RateLimitError()
        assert error.status == 429


class TestInternalServerError:
    """Tests for InternalServerError."""

    def test_status_is_500(self) -> None:
        """Should have 500 status."""
        error = InternalServerError()
        assert error.status == 500


class TestWebSocketError:
    """Tests for WebSocketError."""

    def test_stores_request_id(self) -> None:
        """Should store request_id."""
        error = WebSocketError("error", "req-123")
        assert error.request_id == "req-123"

    def test_request_id_optional(self) -> None:
        """Should work without request_id."""
        error = WebSocketError("error")
        assert error.request_id is None
