"""WebSocket message type definitions."""

from typing import Literal, TypedDict

from polymarket_us.types import Amount, Execution, Order, UserPosition

PrivateSubscriptionType = Literal[
    "SUBSCRIPTION_TYPE_ORDER",
    "SUBSCRIPTION_TYPE_POSITION",
    "SUBSCRIPTION_TYPE_ACCOUNT_BALANCE",
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
    subscriptionType: Literal["SUBSCRIPTION_TYPE_ORDER"]
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
    """Position snapshot message."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_POSITION"]
    positionSubscriptionSnapshot: _PositionSubscriptionSnapshot


class _PositionSubscriptionUpdate(TypedDict):
    marketSlug: str
    position: UserPosition


class PositionUpdate(TypedDict):
    """Position update message."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_POSITION"]
    positionSubscriptionUpdate: _PositionSubscriptionUpdate


class _AccountBalanceSubscriptionSnapshot(TypedDict):
    balance: float
    buyingPower: float


class AccountBalanceSnapshot(TypedDict):
    """Account balance snapshot message."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_ACCOUNT_BALANCE"]
    accountBalanceSubscriptionSnapshot: _AccountBalanceSubscriptionSnapshot


class _AccountBalanceSubscriptionUpdate(TypedDict):
    balance: float
    buyingPower: float


class AccountBalanceUpdate(TypedDict):
    """Account balance update message."""

    requestId: str
    subscriptionType: Literal["SUBSCRIPTION_TYPE_ACCOUNT_BALANCE"]
    accountBalanceSubscriptionUpdate: _AccountBalanceSubscriptionUpdate


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
    | Heartbeat
    | WebSocketErrorMessage
)

MarketMessage = MarketData | MarketDataLite | Trade | Heartbeat | WebSocketErrorMessage
