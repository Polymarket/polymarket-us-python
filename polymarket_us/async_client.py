"""Asynchronous client for Polymarket US API."""

from __future__ import annotations

import asyncio
import uuid
from typing import TYPE_CHECKING, Any

import httpx

from polymarket_us import _retry
from polymarket_us.auth import create_auth_headers
from polymarket_us.client import CORRELATION_ID_HEADER, default_user_agent
from polymarket_us.errors import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)
from polymarket_us.resources import (
    AsyncAccount,
    AsyncEvents,
    AsyncMarkets,
    AsyncOrders,
    AsyncPortfolio,
    AsyncSearch,
    AsyncSeries,
    AsyncSports,
)

if TYPE_CHECKING:
    from polymarket_us.websocket import MarketsWebSocket, PrivateWebSocket

GATEWAY_BASE_URL = "https://gateway.polymarket.us"
API_BASE_URL = "https://api.polymarket.us"


class AsyncPolymarketUS:
    """Asynchronous client for the Polymarket US API."""

    def __init__(
        self,
        *,
        key_id: str | None = None,
        secret_key: str | None = None,
        gateway_base_url: str = GATEWAY_BASE_URL,
        api_base_url: str = API_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = _retry.DEFAULT_MAX_RETRIES,
    ) -> None:
        """Initialize the Polymarket US async client.

        Args:
            key_id: API key ID (required for authenticated endpoints)
            secret_key: Base64-encoded Ed25519 secret key (required for authenticated endpoints)
            gateway_base_url: Base URL for public gateway API
            api_base_url: Base URL for authenticated API
            timeout: Request timeout in seconds
            max_retries: Maximum automatic retries for idempotent requests on
                transient failures (timeouts, connection errors, and 408/409/429/5xx).
                Non-idempotent requests (e.g. order placement) are never retried.
        """
        self.key_id = key_id
        self.secret_key = secret_key
        self.gateway_base_url = gateway_base_url
        self.api_base_url = api_base_url
        self.timeout = timeout
        self.max_retries = max_retries

        self._user_agent = default_user_agent()
        self._http = httpx.AsyncClient(timeout=timeout)

        # Resource instances
        self.events = AsyncEvents(self)
        self.markets = AsyncMarkets(self)
        self.orders = AsyncOrders(self)
        self.portfolio = AsyncPortfolio(self)
        self.account = AsyncAccount(self)
        self.series = AsyncSeries(self)
        self.sports = AsyncSports(self)
        self.search = AsyncSearch(self)
        self.ws = _AsyncWebSocketFactory(self)

    async def get(
        self,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        authenticated: bool = False,
    ) -> Any:
        """Make a GET request."""
        return await self._request("GET", path, query=query, authenticated=authenticated)

    async def post(
        self,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        authenticated: bool = False,
    ) -> Any:
        """Make a POST request."""
        return await self._request(
            "POST", path, query=query, body=body, authenticated=authenticated
        )

    async def delete(
        self,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        authenticated: bool = False,
    ) -> Any:
        """Make a DELETE request."""
        return await self._request("DELETE", path, query=query, authenticated=authenticated)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        authenticated: bool = False,
    ) -> Any:
        """Make an HTTP request, retrying idempotent requests on transient errors."""
        base_url = self.api_base_url if authenticated else self.gateway_base_url
        url = f"{base_url}{path}"

        if authenticated and (not self.key_id or not self.secret_key):
            raise AuthenticationError(
                "API key credentials required for authenticated endpoints. "
                "Provide key_id and secret_key when initializing the client.",
                response=_make_fake_response(401, url),
            )

        params = self._build_query_params(query) if query else None
        correlation_id = str(uuid.uuid4())
        base_headers = {
            "Content-Type": "application/json",
            "User-Agent": self._user_agent,
            CORRELATION_ID_HEADER: correlation_id,
        }

        attempt = 0
        while True:
            headers = dict(base_headers)
            if authenticated:
                headers.update(
                    create_auth_headers(self.key_id, self.secret_key, method, path)  # type: ignore[arg-type]
                )

            try:
                response = await self._http.request(
                    method, url, params=params, json=body, headers=headers
                )
            except httpx.TimeoutException as e:
                if _retry.can_retry_method(method) and attempt < self.max_retries:
                    await asyncio.sleep(_retry.backoff_delay(attempt))
                    attempt += 1
                    continue
                raise APITimeoutError(
                    request=getattr(e, "_request", None), request_id=correlation_id
                )
            except httpx.TransportError as e:
                if _retry.can_retry_method(method) and attempt < self.max_retries:
                    await asyncio.sleep(_retry.backoff_delay(attempt))
                    attempt += 1
                    continue
                raise APIConnectionError(
                    message=str(e), request=getattr(e, "_request", None), request_id=correlation_id
                )

            if response.is_success:
                if not response.text:
                    return {}
                return response.json()

            if (
                _retry.is_retryable_status(response.status_code)
                and _retry.can_retry_method(method)
                and attempt < self.max_retries
            ):
                retry_after = _retry.retry_after_seconds(response.headers.get("Retry-After"))
                await asyncio.sleep(_retry.backoff_delay(attempt, retry_after))
                attempt += 1
                continue

            self._handle_error_response(response, correlation_id)

    def _build_query_params(
        self, query: dict[str, Any]
    ) -> list[tuple[str, str | int | float | bool | None]]:
        """Build query params, handling arrays and filtering None."""
        params: list[tuple[str, str | int | float | bool | None]] = []
        for key, value in query.items():
            if value is None:
                continue
            if isinstance(value, list):
                for item in value:
                    params.append((key, str(item)))
            elif isinstance(value, bool):
                params.append((key, str(value).lower()))
            else:
                params.append((key, str(value)))
        return params

    def _handle_error_response(
        self, response: httpx.Response, correlation_id: str | None = None
    ) -> None:
        """Raise the appropriate typed error for an unsuccessful response."""
        body: object | None = None
        try:
            body = response.json()
            if isinstance(body, dict):
                message = body.get("message") or body.get("error") or response.reason_phrase
            else:
                message = response.reason_phrase or "Unknown error"
        except Exception:
            message = response.text or response.reason_phrase or "Unknown error"

        request_id = (
            response.headers.get(CORRELATION_ID_HEADER)
            or response.headers.get("x-request-id")
            or correlation_id
        )

        status = response.status_code
        if status == 400:
            raise BadRequestError(message, response=response, body=body, request_id=request_id)
        elif status == 401:
            raise AuthenticationError(message, response=response, body=body, request_id=request_id)
        elif status == 403:
            raise PermissionDeniedError(
                message, response=response, body=body, request_id=request_id
            )
        elif status == 404:
            raise NotFoundError(message, response=response, body=body, request_id=request_id)
        elif status == 429:
            raise RateLimitError(message, response=response, body=body, request_id=request_id)
        elif status >= 500:
            raise InternalServerError(message, response=response, body=body, request_id=request_id)
        else:
            raise APIStatusError(message, response=response, body=body, request_id=request_id)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncPolymarketUS:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()


class _AsyncWebSocketFactory:
    """Factory for creating WebSocket connections."""

    def __init__(self, client: AsyncPolymarketUS) -> None:
        self._client = client

    def _get_ws_options(self) -> dict[str, str]:
        if not self._client.key_id or not self._client.secret_key:
            raise AuthenticationError(
                "API key credentials required for WebSocket connections. "
                "Provide key_id and secret_key when initializing the client.",
                response=_make_fake_response(401, "wss://api.polymarket.us"),
            )
        url = self._client.api_base_url.replace("https://", "wss://").replace("http://", "ws://")
        return {
            "key_id": self._client.key_id,
            "secret_key": self._client.secret_key,
            "base_url": url,
        }

    def private(self) -> PrivateWebSocket:
        """Create a private WebSocket for orders, positions, and balances."""
        from polymarket_us.websocket import PrivateWebSocket

        return PrivateWebSocket(**self._get_ws_options())

    def markets(self) -> MarketsWebSocket:
        """Create a markets WebSocket for order book and trade data."""
        from polymarket_us.websocket import MarketsWebSocket

        return MarketsWebSocket(**self._get_ws_options())


def _make_fake_response(status_code: int, url: str) -> httpx.Response:
    """Create a fake response for errors raised before making a request."""
    return httpx.Response(status_code=status_code, request=httpx.Request("GET", url))
