"""Markets WebSocket."""

import json

from polymarket_us.errors import PolymarketUSError, WebSocketError

from .base import BaseWebSocket
from .types import MarketSubscriptionType


class MarketsWebSocket(BaseWebSocket):
    """WebSocket for market data (order book, trades)."""

    def __init__(self, **kwargs: str) -> None:
        """Initialize markets WebSocket."""
        super().__init__(path="/v1/ws/markets", **kwargs)

    async def subscribe_market_data(self, request_id: str, market_slugs: list[str]) -> None:
        """Subscribe to full order book data.

        Args:
            request_id: Unique request ID
            market_slugs: List of market slugs to subscribe to
        """
        await self.subscribe(request_id, "SUBSCRIPTION_TYPE_MARKET_DATA", market_slugs)

    async def subscribe_market_data_lite(self, request_id: str, market_slugs: list[str]) -> None:
        """Subscribe to lightweight price data.

        Args:
            request_id: Unique request ID
            market_slugs: List of market slugs to subscribe to
        """
        await self.subscribe(request_id, "SUBSCRIPTION_TYPE_MARKET_DATA_LITE", market_slugs)

    async def subscribe_trades(self, request_id: str, market_slugs: list[str]) -> None:
        """Subscribe to trade notifications.

        Args:
            request_id: Unique request ID
            market_slugs: List of market slugs to subscribe to
        """
        await self.subscribe(request_id, "SUBSCRIPTION_TYPE_TRADE", market_slugs)

    async def subscribe_all(
        self,
        request_id: str,
        subscription_type: MarketSubscriptionType,
        market_slugs: list[str],
    ) -> None:
        """Subscribe to any market data type.

        Args:
            request_id: Unique request ID
            subscription_type: Type of subscription
            market_slugs: List of market slugs to subscribe to
        """
        await self.subscribe(request_id, subscription_type, market_slugs)

    def _handle_message(self, data: str) -> None:
        """Handle incoming message."""
        try:
            message = json.loads(data)
        except json.JSONDecodeError:
            self._emit("error", PolymarketUSError(f"Failed to parse message: {data}"))
            return

        self._emit("message", message)

        if "heartbeat" in message:
            self._emit("heartbeat")
        elif "error" in message:
            self._emit(
                "error",
                WebSocketError(message["error"], message.get("requestId")),
            )
        elif "marketData" in message:
            self._emit("market_data", message)
        elif "marketDataLite" in message:
            self._emit("market_data_lite", message)
        elif "trade" in message:
            self._emit("trade", message)
