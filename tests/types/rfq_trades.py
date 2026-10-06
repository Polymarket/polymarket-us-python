"""Typed consumers of the RFQ trade-history and live trade contracts."""

from decimal import Decimal

from polymarket_us import AsyncPolymarketUS, PolymarketUS
from polymarket_us.types import GetRFQTradesParams, GetRFQTradesResponse, RFQSide, RFQTrade
from polymarket_us.websocket import PrivateMessage, RFQEvent

trade: RFQTrade = {
    "tradeId": "trade-1",
    "symbol": "Combo-A",
    "price": "0.123400000000000001",
    "qtyDecimal": "0.010000000000000001",
    "aggressorSide": "SIDE_BUY",
    "executedTime": "2026-10-04T12:00:00.123456789Z",
}

frames: list[RFQEvent] = [
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {"rfqTrade": {"trade": trade}},
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {
            "rfqTrade": {
                "trade": {
                    "tradeId": "",
                    "symbol": "",
                    "price": "",
                    "qtyDecimal": "",
                    "aggressorSide": "SIDE_UNDEFINED",
                    "executedTime": None,
                }
            }
        },
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {"rfqTrade": {"trade": None}},
    },
]
messages: list[PrivateMessage] = [*frames]
params: GetRFQTradesParams = {
    "limit": 2,
    "cursor": "opaque+/=cursor",
    "startTime": "2026-10-04T00:00:00.123456789Z",
    "endTime": "2026-10-05T00:00:00.123456789Z",
    "symbol": "Combo-A",
}
page: GetRFQTradesResponse = {"trades": [trade], "cursor": ""}


def read_trade(value: RFQTrade) -> tuple[str, str, Decimal, Decimal, RFQSide, str | None]:
    return (
        value["tradeId"],
        value["symbol"],
        Decimal(value["price"]),
        Decimal(value["qtyDecimal"]),
        value["aggressorSide"],
        value["executedTime"],
    )


def live_trade(event: RFQEvent) -> RFQTrade | None:
    payload = event["rfqEvent"].get("rfqTrade")
    return payload["trade"] if payload is not None else None


def history(client: PolymarketUS) -> list[RFQTrade]:
    result: GetRFQTradesResponse = client.rfqs.trades(params)
    if result["cursor"]:
        result = client.rfqs.trades({**params, "cursor": result["cursor"]})
    return result["trades"]


async def async_history(client: AsyncPolymarketUS) -> list[RFQTrade]:
    result: GetRFQTradesResponse = await client.rfqs.trades(params)
    if result["cursor"]:
        result = await client.rfqs.trades({**params, "cursor": result["cursor"]})
    return result["trades"]
