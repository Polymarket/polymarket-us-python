"""Typed consumers of WebSocket error context, including unknown subscriptions."""

from polymarket_us import WebSocketError
from polymarket_us.websocket import WebSocketErrorMessage

legacy_frame: WebSocketErrorMessage = {"error": "subscription failed"}
frame: WebSocketErrorMessage = {
    "error": "subscription failed",
    "requestId": "req-123",
    "subscriptionType": "SUBSCRIPTION_TYPE_FUTURE",
}
error = WebSocketError(
    frame["error"],
    frame.get("requestId"),
    subscription_type=frame.get("subscriptionType"),
)
subscription_type: str | None = error.subscription_type
