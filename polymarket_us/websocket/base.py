"""Base WebSocket class."""

from __future__ import annotations

import asyncio
import contextlib
import json
from collections.abc import Callable
from typing import Any

import websockets
from websockets.asyncio.client import ClientConnection

from polymarket_us.auth import create_auth_headers
from polymarket_us.errors import PolymarketUSError

from .types import MarketSubscriptionType, PrivateSubscriptionType


class BaseWebSocket:
    """Base WebSocket class with event emitter pattern."""

    def __init__(
        self,
        *,
        key_id: str,
        secret_key: str,
        base_url: str = "wss://api.polymarket.us",
        path: str,
    ) -> None:
        """Initialize WebSocket.

        Args:
            key_id: API key ID
            secret_key: Base64-encoded Ed25519 secret key
            base_url: WebSocket base URL
            path: WebSocket endpoint path
        """
        self.key_id = key_id
        self.secret_key = secret_key
        self.base_url = base_url
        self.path = path
        self._ws: ClientConnection | None = None
        self._listeners: dict[str, list[Callable[..., Any]]] = {}
        self._once_listeners: dict[str, list[Callable[..., Any]]] = {}
        self._message_task: asyncio.Task[None] | None = None

    async def connect(self) -> None:
        """Establish WebSocket connection."""
        url = f"{self.base_url}{self.path}"
        headers = create_auth_headers(self.key_id, self.secret_key, "GET", self.path)

        self._ws = await websockets.connect(url, additional_headers=headers)
        self._emit("open")

        # Start message handler
        self._message_task = asyncio.create_task(self._message_loop())

    async def _message_loop(self) -> None:
        """Process incoming messages."""
        if not self._ws:
            return
        try:
            async for message in self._ws:
                if isinstance(message, bytes):
                    message = message.decode("utf-8")
                self._handle_message(message)
        except websockets.ConnectionClosed:
            self._emit("close")
        except Exception as e:
            self._emit("error", PolymarketUSError(str(e)))

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

    async def unsubscribe(self, request_id: str) -> None:
        """Unsubscribe from a data stream.

        Args:
            request_id: Request ID of the subscription to cancel
        """
        await self.send({"unsubscribe": {"requestId": request_id}})

    async def close(self) -> None:
        """Close the WebSocket connection."""
        if self._message_task:
            self._message_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._message_task
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
