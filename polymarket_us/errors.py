"""Exception classes for Polymarket US SDK."""

import httpx


class PolymarketUSError(Exception):
    """Base exception for Polymarket US SDK errors."""

    pass


class APIError(PolymarketUSError):
    """Error returned by the API."""

    message: str
    request: httpx.Request | None
    body: object | None
    request_id: str | None

    def __init__(
        self,
        message: str,
        *,
        request: httpx.Request | None = None,
        body: object | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.request = request
        self.body = body
        self.request_id = request_id

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(message={self.message!r}, request_id={self.request_id!r})"
        )


class APIConnectionError(APIError):
    """Network connection error."""

    def __init__(
        self,
        *,
        message: str = "Connection error.",
        request: httpx.Request | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message, request=request, body=None, request_id=request_id)


class APITimeoutError(APIConnectionError):
    """Request timed out."""

    def __init__(
        self, *, request: httpx.Request | None = None, request_id: str | None = None
    ) -> None:
        super().__init__(message="Request timed out.", request=request, request_id=request_id)


class APIStatusError(APIError):
    """HTTP 4xx/5xx response."""

    response: httpx.Response
    status_code: int

    def __init__(
        self,
        message: str,
        *,
        response: httpx.Response,
        body: object | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message, request=response.request, body=body, request_id=request_id)
        self.response = response
        self.status_code = response.status_code

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(status_code={self.status_code}, "
            f"message={self.message!r}, request_id={self.request_id!r})"
        )


class BadRequestError(APIStatusError):
    """Bad request (400)."""

    pass


class AuthenticationError(APIStatusError):
    """Authentication failed (401)."""

    pass


class PermissionDeniedError(APIStatusError):
    """Permission denied (403)."""

    pass


class NotFoundError(APIStatusError):
    """Resource not found (404)."""

    pass


class RateLimitError(APIStatusError):
    """Rate limit exceeded (429)."""

    pass


class InternalServerError(APIStatusError):
    """Internal server error (500+)."""

    pass


class WebSocketError(PolymarketUSError):
    """WebSocket-related error."""

    def __init__(self, message: str, request_id: str | None = None) -> None:
        super().__init__(message)
        self.request_id = request_id

    def __repr__(self) -> str:
        return f"WebSocketError(message={str(self)!r}, request_id={self.request_id!r})"
