"""Typed consumers of gateway RFQ frames and exact portfolio quantities.

Fixtures were serialized from gateway eb891a3e with protojson EmitUnpopulated.
"""

from decimal import Decimal

from polymarket_us.types import (
    RFQ,
    Activity,
    Quote,
    QuoteStatus,
    RFQComboLeg,
    RFQSide,
    RFQStatus,
    Trade,
)
from polymarket_us.websocket import PrivateMessage, PrivateSubscriptionType, RFQEvent

frames: list[RFQEvent] = [
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {
            "rfqCreated": {
                "rfq": {
                    "id": "rfq-1",
                    "qtyDecimal": "0.0100",
                    "symbol": "combo-example",
                    "rfqCreatorUserId": "requester-1",
                    "createdTime": "2026-09-28T12:00:00.123456789Z",
                    "restRemainder": False,
                    "status": "RFQ_STATUS_OPEN",
                    "updatedTime": "2026-09-28T12:00:01.123456789Z",
                    "comboLegs": [
                        {"symbol": "market-a", "side": "SIDE_BUY", "settlementPrice": "0"},
                        {"symbol": "market-b", "side": "SIDE_SELL"},
                    ],
                    "tickSize": 0.0001,
                }
            }
        },
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {
            "rfqClosed": {
                "rfq": {
                    "id": "rfq-1",
                    "cashOrderQty": "12.3400",
                    "symbol": "combo-example",
                    "rfqCreatorUserId": "requester-1",
                    "createdTime": "2026-09-28T12:00:00.123456789Z",
                    "restRemainder": False,
                    "status": "RFQ_STATUS_CLOSED",
                    "updatedTime": "2026-09-28T12:00:01.123456789Z",
                    "comboLegs": [
                        {"symbol": "market-a", "side": "SIDE_BUY", "settlementPrice": "0"},
                        {"symbol": "market-b", "side": "SIDE_SELL"},
                    ],
                    "tickSize": 0.0001,
                }
            }
        },
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {
            "quoteCreated": {
                "quote": {
                    "id": "quote-1",
                    "rfqId": "rfq-1",
                    "creatorRfqUserId": "quoter-1",
                    "symbol": "combo-example",
                    "status": "QUOTE_STATUS_ACTIVE",
                    "createdTime": "2026-09-28T12:00:00.123456789Z",
                    "buyPrice": "0.1234",
                    "sellPrice": "0.8766",
                    "restRemainder": True,
                    "postOnly": False,
                    "rfqCreatorUserId": "requester-1",
                    "rfqCashOrderQty": "12.3400",
                    "buyQtyDecimal": "19.6000",
                    "sellQtyDecimal": "0.0100",
                    "updatedTime": "2026-09-28T12:00:01.123456789Z",
                    "acceptedSide": "SIDE_UNDEFINED",
                    "acceptedTime": None,
                    "confirmedTime": None,
                    "confirmationDeadline": None,
                    "executionDeadline": None,
                    "executedTime": None,
                }
            }
        },
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {
            "quoteDeleted": {
                "quote": {
                    "id": "quote-1",
                    "rfqId": "rfq-1",
                    "creatorRfqUserId": "quoter-1",
                    "symbol": "combo-example",
                    "status": "QUOTE_STATUS_DELETED",
                    "createdTime": "2026-09-28T12:00:00.123456789Z",
                    "buyPrice": "0.1234",
                    "sellPrice": "0.8766",
                    "restRemainder": True,
                    "postOnly": False,
                    "rfqCreatorUserId": "requester-1",
                    "rfqCashOrderQty": "12.3400",
                    "buyQtyDecimal": "19.6000",
                    "sellQtyDecimal": "0.0100",
                    "updatedTime": "2026-09-28T12:00:01.123456789Z",
                    "acceptedSide": "SIDE_UNDEFINED",
                    "acceptedTime": None,
                    "confirmedTime": None,
                    "confirmationDeadline": None,
                    "executionDeadline": None,
                    "executedTime": None,
                }
            }
        },
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {
            "quoteAccepted": {
                "quote": {
                    "id": "quote-1",
                    "rfqId": "rfq-1",
                    "creatorRfqUserId": "quoter-1",
                    "symbol": "combo-example",
                    "status": "QUOTE_STATUS_ACCEPTED",
                    "createdTime": "2026-09-28T12:00:00.123456789Z",
                    "buyPrice": "0.1234",
                    "sellPrice": "0.8766",
                    "restRemainder": True,
                    "postOnly": False,
                    "rfqCreatorUserId": "requester-1",
                    "rfqCashOrderQty": "12.3400",
                    "buyQtyDecimal": "19.6000",
                    "sellQtyDecimal": "0.0100",
                    "updatedTime": "2026-09-28T12:00:01.123456789Z",
                    "acceptedSide": "SIDE_BUY",
                    "acceptedTime": "2026-09-28T12:00:02.123456789Z",
                    "confirmedTime": None,
                    "confirmationDeadline": "2026-09-28T12:00:10.123456789Z",
                    "executionDeadline": None,
                    "executedTime": None,
                },
                "confirmationDeadline": "2026-09-28T12:00:10.123456789Z",
            }
        },
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {
            "quoteConfirmed": {
                "quote": {
                    "id": "quote-1",
                    "rfqId": "rfq-1",
                    "creatorRfqUserId": "quoter-1",
                    "symbol": "combo-example",
                    "status": "QUOTE_STATUS_CONFIRMED",
                    "createdTime": "2026-09-28T12:00:00.123456789Z",
                    "buyPrice": "0.1234",
                    "sellPrice": "0.8766",
                    "restRemainder": True,
                    "postOnly": False,
                    "rfqCreatorUserId": "requester-1",
                    "rfqCashOrderQty": "12.3400",
                    "buyQtyDecimal": "19.6000",
                    "sellQtyDecimal": "0.0100",
                    "updatedTime": "2026-09-28T12:00:01.123456789Z",
                    "acceptedSide": "SIDE_BUY",
                    "acceptedTime": "2026-09-28T12:00:02.123456789Z",
                    "confirmedTime": "2026-09-28T12:00:03.123456789Z",
                    "confirmationDeadline": "2026-09-28T12:00:10.123456789Z",
                    "executionDeadline": "2026-09-28T12:00:11.123456789Z",
                    "executedTime": None,
                },
                "executionDeadline": "2026-09-28T12:00:11.123456789Z",
            }
        },
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {
            "quoteExecuted": {
                "quote": {
                    "id": "quote-1",
                    "rfqId": "rfq-1",
                    "creatorRfqUserId": "quoter-1",
                    "symbol": "combo-example",
                    "status": "QUOTE_STATUS_EXECUTED",
                    "createdTime": "2026-09-28T12:00:00.123456789Z",
                    "buyPrice": "0.1234",
                    "sellPrice": "0.8766",
                    "restRemainder": True,
                    "postOnly": False,
                    "rfqCreatorUserId": "requester-1",
                    "rfqCashOrderQty": "12.3400",
                    "buyQtyDecimal": "19.6000",
                    "sellQtyDecimal": "0.0100",
                    "updatedTime": "2026-09-28T12:00:01.123456789Z",
                    "acceptedSide": "SIDE_BUY",
                    "acceptedTime": "2026-09-28T12:00:02.123456789Z",
                    "confirmedTime": "2026-09-28T12:00:03.123456789Z",
                    "confirmationDeadline": "2026-09-28T12:00:10.123456789Z",
                    "executionDeadline": "2026-09-28T12:00:11.123456789Z",
                    "executedTime": "2026-09-28T12:00:11.123456789Z",
                    "rfqCreatorOrderId": "requester-order-1",
                    "creatorOrderId": "quoter-order-1",
                },
                "orderId": "own-order-1",
                "clientOrderId": "own-client-order-1",
                "executedTime": "2026-09-28T12:00:11.123456789Z",
            }
        },
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {
            "rfqCreated": {
                "rfq": {
                    "id": "",
                    "symbol": "",
                    "rfqCreatorUserId": "",
                    "createdTime": None,
                    "restRemainder": False,
                    "status": "RFQ_STATUS_UNSPECIFIED",
                    "updatedTime": None,
                    "comboLegs": [{"symbol": "", "side": "SIDE_UNDEFINED"}],
                }
            }
        },
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {
            "quoteCreated": {
                "quote": {
                    "id": "",
                    "rfqId": "",
                    "creatorRfqUserId": "",
                    "symbol": "",
                    "status": "QUOTE_STATUS_UNDEFINED",
                    "createdTime": None,
                    "buyPrice": "",
                    "sellPrice": "",
                    "restRemainder": False,
                    "postOnly": False,
                    "rfqCreatorUserId": "",
                    "buyQtyDecimal": "",
                    "sellQtyDecimal": "",
                    "updatedTime": None,
                    "acceptedSide": "SIDE_UNDEFINED",
                    "acceptedTime": None,
                    "confirmedTime": None,
                    "confirmationDeadline": None,
                    "executionDeadline": None,
                    "executedTime": None,
                }
            }
        },
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {"rfqCreated": {"rfq": None}},
    },
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {"quoteAccepted": {"quote": None, "confirmationDeadline": None}},
    },
    {"requestId": "rfqs", "subscriptionType": "SUBSCRIPTION_TYPE_RFQ", "rfqEvent": {}},
    {
        "requestId": "rfqs",
        "subscriptionType": "SUBSCRIPTION_TYPE_RFQ",
        "rfqEvent": {"rfqCreated": {"rfq": None}},
    },
    {"requestId": "rfqs", "subscriptionType": "SUBSCRIPTION_TYPE_RFQ", "rfqEvent": {}},
]

subscription: PrivateSubscriptionType = "SUBSCRIPTION_TYPE_RFQ"
messages: list[PrivateMessage] = [*frames]
side: RFQSide = "SIDE_BUY"
status: RFQStatus = "RFQ_STATUS_CLOSED"
quote_status: QuoteStatus = "QUOTE_STATUS_EXECUTED"
leg: RFQComboLeg = {"symbol": "market-a", "side": side, "settlementPrice": "0"}
trade: Trade = {"qty": "0", "qtyDecimal": "0.0100"}
activity: Activity = {"trade": trade}


def exact_trade_quantity(data: Activity) -> Decimal | None:
    value = data.get("trade", {}).get("qtyDecimal")
    return Decimal(value) if value is not None else None


def created_rfq(data: RFQEvent) -> RFQ | None:
    created = data["rfqEvent"].get("rfqCreated")
    return created["rfq"] if created is not None else None


def executed_quote(data: RFQEvent) -> tuple[Quote | None, str, str | None] | None:
    executed = data["rfqEvent"].get("quoteExecuted")
    if executed is None:
        return None
    return executed["quote"], executed["orderId"], executed["executedTime"]
