"""Exception classes for Polymarket US SDK."""


class PolymarketUSError(Exception):
    """Base exception for Polymarket US SDK errors."""

    pass


class APIError(PolymarketUSError):
    """Error returned by the API."""

    def __init__(self, status: int, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.code = code

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(status={self.status}, message={str(self)!r})"


class AuthenticationError(APIError):
    """Authentication failed (401)."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(401, message, "authentication_error")


class BadRequestError(APIError):
    """Bad request (400)."""

    def __init__(self, message: str = "Bad request") -> None:
        super().__init__(400, message, "bad_request")


class NotFoundError(APIError):
    """Resource not found (404)."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(404, message, "not_found")


class RateLimitError(APIError):
    """Rate limit exceeded (429)."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(429, message, "rate_limit_exceeded")


class InternalServerError(APIError):
    """Internal server error (500+)."""

    def __init__(self, message: str = "Internal server error") -> None:
        super().__init__(500, message, "internal_server_error")


class WebSocketError(PolymarketUSError):
    """WebSocket-related error."""

    def __init__(self, message: str, request_id: str | None = None) -> None:
        super().__init__(message)
        self.request_id = request_id

    def __repr__(self) -> str:
        return f"WebSocketError(message={str(self)!r}, request_id={self.request_id!r})"
