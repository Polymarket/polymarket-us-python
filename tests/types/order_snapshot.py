"""Consumer typing checks included in the existing mypy CI job."""

from polymarket_us.websocket.private import PrivateWebSocket
from polymarket_us.websocket.types import OrderSnapshot


async def request_snapshot(ws: PrivateWebSocket) -> None:
    await ws.subscribe("snapshot-1", "SUBSCRIPTION_TYPE_ORDER_SNAPSHOT")


terminal: OrderSnapshot = {
    "requestId": "snapshot-1",
    "subscriptionType": "SUBSCRIPTION_TYPE_ORDER_SNAPSHOT",
    "orderSubscriptionSnapshot": {"orders": [], "eof": True},
}
