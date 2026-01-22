"""Private WebSocket."""

import json

from polymarket_us.errors import PolymarketUSError, WebSocketError

from .base import BaseWebSocket
from .types import PrivateSubscriptionType


class PrivateWebSocket(BaseWebSocket):
    """WebSocket for private data (orders, positions, balances)."""

    def __init__(self, **kwargs: str) -> None:
        """Initialize private WebSocket."""
        super().__init__(path="/v1/ws/private", **kwargs)

    async def subscribe_orders(
        self, request_id: str, market_slugs: list[str] | None = None
    ) -> None:
        """Subscribe to order updates.

        Args:
            request_id: Unique request ID
            market_slugs: Optional list of market slugs to filter
        """
        await self.subscribe(request_id, "SUBSCRIPTION_TYPE_ORDER", market_slugs)

    async def subscribe_positions(
        self, request_id: str, market_slugs: list[str] | None = None
    ) -> None:
        """Subscribe to position updates.

        Args:
            request_id: Unique request ID
            market_slugs: Optional list of market slugs to filter
        """
        await self.subscribe(request_id, "SUBSCRIPTION_TYPE_POSITION", market_slugs)

    async def subscribe_account_balance(self, request_id: str) -> None:
        """Subscribe to account balance updates.

        Args:
            request_id: Unique request ID
        """
        await self.subscribe(request_id, "SUBSCRIPTION_TYPE_ACCOUNT_BALANCE")

    async def subscribe_all(
        self,
        request_id: str,
        subscription_type: PrivateSubscriptionType,
        market_slugs: list[str] | None = None,
    ) -> None:
        """Subscribe to any private data type.

        Args:
            request_id: Unique request ID
            subscription_type: Type of subscription
            market_slugs: Optional list of market slugs to filter
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
        elif "orderSubscriptionSnapshot" in message or "ordersSnapshot" in message:
            self._emit("order_snapshot", message)
        elif "orderSubscriptionUpdate" in message or "orderUpdate" in message:
            self._emit("order_update", message)
        elif "positionSubscriptionSnapshot" in message or "positionsSnapshot" in message:
            self._emit("position_snapshot", message)
        elif "positionSubscriptionUpdate" in message or "positionUpdate" in message:
            self._emit("position_update", message)
        elif (
            "accountBalanceSubscriptionSnapshot" in message or "accountBalancesSnapshot" in message
        ):
            self._emit("account_balance_snapshot", message)
        elif "accountBalanceSubscriptionUpdate" in message or "accountBalanceUpdate" in message:
            self._emit("account_balance_update", message)
