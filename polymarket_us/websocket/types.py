"""WebSocket message type definitions."""

from typing import Literal, TypedDict

from polymarket_us.types import (
    RFQ,
    Amount,
    Execution,
    Order,
    Quote,
    RFQTrade,
    UserBalance,
    UserPosition,
)

PrivateSubscriptionType = Literal[
    "SUBSCRIPTION_TYPE_ORDER",
    "SUBSCRIPTION_TYPE_ORDER_SNAPSHOT",
    "SUBSCRIPTION_TYPE_POSITION",
    "SUBSCRIPTION_TYPE_ACCOUNT_BALANCE",
    "SUBSCRIPTION_TYPE_RFQ",
]

MarketSubscriptionType = Literal[
    "SUBSCRIPTION_TYPE_MARKET_DATA",
    "SUBSCRIPTION_TYPE_MARKET_DATA_LITE",
    "SUBSCRIPTION_TYPE_TRADE",
]


class _SubscribePayload(TypedDict, total=False):
    requestId: str
    subscriptionType: PrivateSubscriptionType | MarketSubscriptionType
    marketSlugs: list[str]


class SubscribeRequest(TypedDict):
    """Subscribe request message."""

    subscribe: _SubscribePayload


class _UnsubscribePayload(TypedDict):
    requestId: str


class UnsubscribeRequest(TypedDict):
    """Unsubscribe request message."""

    unsubscribe: _UnsubscribePayload


WebSocketRequest = SubscribeRequest | UnsubscribeRequest


class _OrderSubscriptionSnapshot(TypedDict):
    orders: list[Order]
    eof: bool


class OrderSnapshot(TypedDict):
    """Order snapshot message."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_ORDER_SNAPSHOT"]
    orderSubscriptionSnapshot: _OrderSubscriptionSnapshot


class _OrderSubscriptionUpdate(TypedDict):
    execution: Execution


class OrderUpdate(TypedDict):
    """Order update message."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_ORDER"]
    orderSubscriptionUpdate: _OrderSubscriptionUpdate


class _PositionSubscriptionSnapshot(TypedDict):
    positions: dict[str, UserPosition]
    eof: bool


class PositionSnapshot(TypedDict):
    """Legacy position snapshot; the current gateway sends updates only."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_POSITION"]
    positionSubscriptionSnapshot: _PositionSubscriptionSnapshot


class _PositionSubscription(TypedDict):
    beforePosition: UserPosition | None
    afterPosition: UserPosition | None
    updateTime: str | None
    entryType: str
    tradeId: str
    referenceId: str
    description: str
    allocationGroupId: str
    transferReferenceTradeIds: list[str]
    shortTransfer: bool
    updateTradeDate: str | None


class PositionUpdate(TypedDict):
    """Position change in the current gateway wire format."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_POSITION"]
    positionSubscription: _PositionSubscription


class _AccountBalancesSnapshot(TypedDict):
    balances: list[UserBalance]


class AccountBalanceSnapshot(TypedDict):
    """Account balance snapshot in the current gateway wire format."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_ACCOUNT_BALANCE"]
    accountBalancesSnapshot: _AccountBalancesSnapshot


class _BalanceChange(TypedDict):
    beforeBalance: UserBalance | None
    afterBalance: UserBalance | None
    description: str
    updateTime: str | None
    modifiedSecurityId: str
    entryType: str
    accountName: str
    id: str


class _AccountBalancesUpdate(TypedDict):
    balanceChange: _BalanceChange


class AccountBalanceUpdate(TypedDict):
    """Account balance change in the current gateway wire format."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_ACCOUNT_BALANCE"]
    accountBalancesUpdate: _AccountBalancesUpdate


class _RFQChange(TypedDict):
    rfq: RFQ | None


class _QuoteChange(TypedDict):
    quote: Quote | None


class _QuoteAccepted(_QuoteChange):
    confirmationDeadline: str | None


class _QuoteConfirmed(_QuoteChange):
    executionDeadline: str | None


class _QuoteExecuted(_QuoteChange):
    orderId: str
    clientOrderId: str
    executedTime: str | None


class _RFQTradeEvent(TypedDict):
    trade: RFQTrade | None


class _RFQEventPayload(TypedDict, total=False):
    # The gateway emits only the selected event; unknown future events may be empty.
    rfqCreated: _RFQChange
    rfqClosed: _RFQChange
    quoteCreated: _QuoteChange
    quoteDeleted: _QuoteChange
    quoteAccepted: _QuoteAccepted
    quoteConfirmed: _QuoteConfirmed
    quoteExecuted: _QuoteExecuted
    rfqTrade: _RFQTradeEvent


class RFQEvent(TypedDict):
    """Private RFQ event in the gateway wire format."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_RFQ"]
    rfqEvent: _RFQEventPayload


class _OrderBookLevel(TypedDict):
    px: Amount
    qty: str


class _MarketDataStats(TypedDict, total=False):
    lastTradePx: Amount
    sharesTraded: str
    openInterest: str
    highPx: Amount
    lowPx: Amount


class _MarketDataPayload(TypedDict, total=False):
    marketSlug: str
    bids: list[_OrderBookLevel]
    offers: list[_OrderBookLevel]
    state: str
    stats: _MarketDataStats
    transactTime: str


class MarketData(TypedDict):
    """Market data message (full order book)."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_MARKET_DATA"]
    marketData: _MarketDataPayload


class _MarketDataLitePayload(TypedDict, total=False):
    marketSlug: str
    bestBid: Amount
    bestAsk: Amount
    lastTradePx: Amount


class MarketDataLite(TypedDict):
    """Market data lite message (best prices only)."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_MARKET_DATA_LITE"]
    marketDataLite: _MarketDataLitePayload


class _TradeSide(TypedDict):
    side: str
    intent: str


class _TradePayload(TypedDict):
    marketSlug: str
    price: Amount
    quantity: Amount
    tradeTime: str
    maker: _TradeSide
    taker: _TradeSide


class Trade(TypedDict):
    """Trade message."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_TRADE"]
    trade: _TradePayload


class Heartbeat(TypedDict):
    """Heartbeat message."""

    heartbeat: dict[str, object]


class WebSocketErrorMessage(TypedDict, total=False):
    """Error message."""

    requestId: str
    error: str


PrivateMessage = (
    OrderSnapshot
    | OrderUpdate
    | PositionSnapshot
    | PositionUpdate
    | AccountBalanceSnapshot
    | AccountBalanceUpdate
    | RFQEvent
    | Heartbeat
    | WebSocketErrorMessage
)

MarketMessage = MarketData | MarketDataLite | Trade | Heartbeat | WebSocketErrorMessage
