"""Base WebSocket class with automatic reconnect and resubscribe."""

from __future__ import annotations

import asyncio
import contextlib
import json
import random
from collections.abc import Callable
from typing import Any

import websockets
from websockets.asyncio.client import ClientConnection

from polymarket_us.auth import create_auth_headers
from polymarket_us.errors import PolymarketUSError

from .types import MarketSubscriptionType, PrivateSubscriptionType

# WebSocket upgrade failures with these statuses are fatal (bad credentials or
# rate limiting) and must not trigger reconnect attempts.
_FATAL_AUTH_STATUSES = frozenset({401, 403, 429})

_RECONNECT_INITIAL_SECONDS = 0.5
_RECONNECT_MAX_SECONDS = 30.0


def _reconnect_delay(attempt: int) -> float:
    """Exponential reconnect backoff with equal jitter (attempt is 0-indexed)."""
    capped = min(_RECONNECT_INITIAL_SECONDS * (2**attempt), _RECONNECT_MAX_SECONDS)
    return capped / 2 + random.random() * (capped / 2)


def _upgrade_status(exc: Exception) -> int | None:
    """Extract the HTTP status from a failed WebSocket upgrade, if available.

    Handles both the modern (``exc.response.status_code``) and legacy
    (``exc.status_code``) ``websockets`` exception shapes.
    """
    response = getattr(exc, "response", None)
    if response is not None:
        status = getattr(response, "status_code", None)
        if isinstance(status, int):
            return status
    status = getattr(exc, "status_code", None)
    return status if isinstance(status, int) else None


class _Subscription:
    """A subscription the client should replay after a reconnect."""

    def __init__(
        self,
        subscription_type: PrivateSubscriptionType | MarketSubscriptionType,
        market_slugs: list[str] | None,
    ) -> None:
        self.subscription_type = subscription_type
        self.market_slugs = market_slugs


class BaseWebSocket:
    """Base WebSocket class with an event emitter and resilient connection."""

    def __init__(
        self,
        *,
        key_id: str,
        secret_key: str,
        base_url: str = "wss://api.polymarket.us",
        path: str,
        auto_reconnect: bool = True,
        reconnect_max_attempts: int | None = None,
    ) -> None:
        """Initialize WebSocket.

        Args:
            key_id: API key ID
            secret_key: Base64-encoded Ed25519 secret key
            base_url: WebSocket base URL
            path: WebSocket endpoint path
            auto_reconnect: Reconnect and replay subscriptions on unexpected drops
            reconnect_max_attempts: Max reconnect attempts per drop (None = unlimited)
        """
        self.key_id = key_id
        self.secret_key = secret_key
        self.base_url = base_url
        self.path = path
        self.auto_reconnect = auto_reconnect
        self.reconnect_max_attempts = reconnect_max_attempts
        self._ws: ClientConnection | None = None
        self._listeners: dict[str, list[Callable[..., Any]]] = {}
        self._once_listeners: dict[str, list[Callable[..., Any]]] = {}
        self._run_task: asyncio.Task[None] | None = None
        self._subscriptions: dict[str, _Subscription] = {}
        self._closed = False

    async def connect(self) -> None:
        """Establish the WebSocket connection and start processing messages."""
        self._closed = False
        await self._open_socket()
        self._emit("open")
        self._run_task = asyncio.create_task(self._run())

    async def _open_socket(self) -> None:
        """Open a socket with a freshly signed auth handshake."""
        url = f"{self.base_url}{self.path}"
        # Re-sign on every (re)connect: the timestamp must be within the skew window.
        headers = create_auth_headers(self.key_id, self.secret_key, "GET", self.path)
        self._ws = await websockets.connect(url, additional_headers=headers)

    async def _run(self) -> None:
        """Read messages, reconnecting and resubscribing on unexpected drops."""
        while True:
            try:
                if self._ws is None:
                    break
                async for message in self._ws:
                    if isinstance(message, bytes):
                        message = message.decode("utf-8")
                    self._handle_message(message)
            except websockets.ConnectionClosed:
                pass
            except Exception as e:
                self._emit("error", PolymarketUSError(str(e)))

            # The loop may have exited on a still-open socket (e.g. a handler
            # error rather than a drop). Close it before reconnecting so the old
            # connection isn't leaked when _open_socket overwrites self._ws.
            with contextlib.suppress(Exception):
                if self._ws is not None:
                    await self._ws.close(1000, "OK")

            if self._closed or not self.auto_reconnect:
                if not self._closed:
                    self._emit("close")
                return

            if not await self._reconnect():
                if not self._closed:
                    self._emit("close")
                return

    async def _reconnect(self) -> bool:
        """Reconnect with backoff and replay subscriptions. Returns success."""
        attempt = 0
        while not self._closed and (
            self.reconnect_max_attempts is None or attempt < self.reconnect_max_attempts
        ):
            await asyncio.sleep(_reconnect_delay(attempt))
            if self._closed:
                return False
            try:
                await self._open_socket()
            except Exception as e:
                status = _upgrade_status(e)
                if status in _FATAL_AUTH_STATUSES:
                    self._emit("error", PolymarketUSError(f"WebSocket auth failed ({status})"))
                    return False
                attempt += 1
                continue
            # The user may have called close() while the upgrade was in flight.
            if self._closed:
                return False
            # If the fresh connection drops mid-replay, treat it as another
            # failed attempt rather than letting the exception kill the task.
            try:
                await self._resubscribe()
            except Exception:
                # Close the just-opened socket before retrying so it isn't
                # orphaned when the next attempt overwrites self._ws.
                with contextlib.suppress(Exception):
                    if self._ws:
                        await self._ws.close(1000, "OK")
                attempt += 1
                continue
            self._emit("reconnect")
            return True
        return False

    async def _resubscribe(self) -> None:
        """Replay all active subscriptions after a reconnect."""
        for request_id, sub in list(self._subscriptions.items()):
            request: dict[str, Any] = {
                "subscribe": {
                    "requestId": request_id,
                    "subscriptionType": sub.subscription_type,
                }
            }
            if sub.market_slugs:
                request["subscribe"]["marketSlugs"] = sub.market_slugs
            await self.send(request)

    def _handle_message(self, data: str) -> None:
        """Handle incoming message (override in subclasses)."""
        raise NotImplementedError

    async def send(self, request: dict[str, Any]) -> None:
        """Send a message to the WebSocket.

        Args:
            request: Message to send
        """
        if not self._ws:
            raise PolymarketUSError("WebSocket is not connected")
        await self._ws.send(json.dumps(request))

    async def subscribe(
        self,
        request_id: str,
        subscription_type: PrivateSubscriptionType | MarketSubscriptionType,
        market_slugs: list[str] | None = None,
    ) -> None:
        """Subscribe to a data stream.

        The subscription is recorded so it can be replayed automatically after a
        reconnect.

        Args:
            request_id: Unique request ID
            subscription_type: Type of subscription
            market_slugs: Optional list of market slugs to subscribe to
        """
        request: dict[str, Any] = {
            "subscribe": {
                "requestId": request_id,
                "subscriptionType": subscription_type,
            }
        }
        if market_slugs:
            request["subscribe"]["marketSlugs"] = market_slugs
        await self.send(request)
        self._subscriptions[request_id] = _Subscription(subscription_type, market_slugs)

    async def unsubscribe(self, request_id: str) -> None:
        """Unsubscribe from a data stream.

        Args:
            request_id: Request ID of the subscription to cancel
        """
        self._subscriptions.pop(request_id, None)
        await self.send({"unsubscribe": {"requestId": request_id}})

    async def close(self) -> None:
        """Close the WebSocket connection and stop reconnecting."""
        self._closed = True
        # Cancel first so an in-flight reconnect (sleeping or mid-handshake) is
        # interrupted rather than left to open a socket close() never sees.
        if self._run_task:
            self._run_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._run_task
            self._run_task = None
        if self._ws:
            await self._ws.close(1000, "OK")
        self._ws = None

    @property
    def is_connected(self) -> bool:
        """Check if WebSocket is connected."""
        return self._ws is not None and self._ws.state.name == "OPEN"

    def on(self, event: str, callback: Callable[..., Any]) -> BaseWebSocket:
        """Register an event listener.

        Args:
            event: Event name
            callback: Callback function

        Returns:
            Self for chaining
        """
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
        return self

    def off(self, event: str, callback: Callable[..., Any]) -> BaseWebSocket:
        """Remove an event listener.

        Args:
            event: Event name
            callback: Callback function to remove

        Returns:
            Self for chaining
        """
        if event in self._listeners:
            self._listeners[event] = [cb for cb in self._listeners[event] if cb != callback]
        return self

    def once(self, event: str, callback: Callable[..., Any]) -> BaseWebSocket:
        """Register a one-time event listener.

        Args:
            event: Event name
            callback: Callback function (called only once)

        Returns:
            Self for chaining
        """
        if event not in self._once_listeners:
            self._once_listeners[event] = []
        self._once_listeners[event].append(callback)
        return self

    def _emit(self, event: str, *args: Any) -> None:
        """Emit an event to listeners.

        Args:
            event: Event name
            *args: Arguments to pass to listeners
        """
        # Regular listeners
        for callback in self._listeners.get(event, []):
            callback(*args)
        # Once listeners (remove after calling)
        once = self._once_listeners.pop(event, [])
        for callback in once:
            callback(*args)
