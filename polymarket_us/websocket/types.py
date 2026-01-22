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
    request_id: str
    subscription_type: PrivateSubscriptionType | MarketSubscriptionType
    market_slugs: list[str]


class SubscribeRequest(TypedDict):
    """Subscribe request message."""

    subscribe: _SubscribePayload


class _UnsubscribePayload(TypedDict):
    request_id: str


class UnsubscribeRequest(TypedDict):
    """Unsubscribe request message."""

    unsubscribe: _UnsubscribePayload


WebSocketRequest = SubscribeRequest | UnsubscribeRequest


class _OrderSubscriptionSnapshot(TypedDict):
    orders: list[Order]
    eof: bool


class OrderSnapshot(TypedDict):
    """Order snapshot message."""

    request_id: str
    subscription_type: Literal["SUBSCRIPTION_TYPE_ORDER"]
    order_subscription_snapshot: _OrderSubscriptionSnapshot


class _OrderSubscriptionUpdate(TypedDict):
    execution: Execution


class OrderUpdate(TypedDict):
    """Order update message."""

    request_id: str
    subscription_type: Literal["SUBSCRIPTION_TYPE_ORDER"]
    order_subscription_update: _OrderSubscriptionUpdate


class _PositionSubscriptionSnapshot(TypedDict):
    positions: dict[str, UserPosition]
    eof: bool


class PositionSnapshot(TypedDict):
    """Position snapshot message."""

    request_id: str
    subscription_type: Literal["SUBSCRIPTION_TYPE_POSITION"]
    position_subscription_snapshot: _PositionSubscriptionSnapshot


class _PositionSubscriptionUpdate(TypedDict):
    market_slug: str
    position: UserPosition


class PositionUpdate(TypedDict):
    """Position update message."""

    request_id: str
    subscription_type: Literal["SUBSCRIPTION_TYPE_POSITION"]
    position_subscription_update: _PositionSubscriptionUpdate


class _AccountBalanceSubscriptionSnapshot(TypedDict):
    balance: float
    buying_power: float


class AccountBalanceSnapshot(TypedDict):
    """Account balance snapshot message."""

    request_id: str
    subscription_type: Literal["SUBSCRIPTION_TYPE_ACCOUNT_BALANCE"]
    account_balance_subscription_snapshot: _AccountBalanceSubscriptionSnapshot


class _AccountBalanceSubscriptionUpdate(TypedDict):
    balance: float
    buying_power: float


class AccountBalanceUpdate(TypedDict):
    """Account balance update message."""

    request_id: str
    subscription_type: Literal["SUBSCRIPTION_TYPE_ACCOUNT_BALANCE"]
    account_balance_subscription_update: _AccountBalanceSubscriptionUpdate


class _OrderBookLevel(TypedDict):
    px: Amount
    qty: str


class _MarketDataStats(TypedDict, total=False):
    last_trade_px: Amount
    shares_traded: str
    open_interest: str
    high_px: Amount
    low_px: Amount


class _MarketDataPayload(TypedDict, total=False):
    market_slug: str
    bids: list[_OrderBookLevel]
    offers: list[_OrderBookLevel]
    state: str
    stats: _MarketDataStats
    transact_time: str


class MarketData(TypedDict):
    """Market data message (full order book)."""

    request_id: str
    subscription_type: Literal["SUBSCRIPTION_TYPE_MARKET_DATA"]
    market_data: _MarketDataPayload


class _MarketDataLitePayload(TypedDict, total=False):
    market_slug: str
    best_bid: Amount
    best_ask: Amount
    last_trade_px: Amount


class MarketDataLite(TypedDict):
    """Market data lite message (best prices only)."""

    request_id: str
    subscription_type: Literal["SUBSCRIPTION_TYPE_MARKET_DATA_LITE"]
    market_data_lite: _MarketDataLitePayload


class _TradeSide(TypedDict):
    side: str
    intent: str


class _TradePayload(TypedDict):
    market_slug: str
    price: Amount
    quantity: Amount
    trade_time: str
    maker: _TradeSide
    taker: _TradeSide


class Trade(TypedDict):
    """Trade message."""

    request_id: str
    subscription_type: Literal["SUBSCRIPTION_TYPE_TRADE"]
    trade: _TradePayload


class Heartbeat(TypedDict):
    """Heartbeat message."""

    heartbeat: dict[str, object]


class WebSocketErrorMessage(TypedDict, total=False):
    """Error message."""

    request_id: str
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
