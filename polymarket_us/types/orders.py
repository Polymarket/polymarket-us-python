"""Orders type definitions."""

from typing import Literal, TypedDict

from polymarket_us.types.common import Amount

OrderType = Literal["ORDER_TYPE_LIMIT", "ORDER_TYPE_MARKET"]
OrderSide = Literal["ORDER_SIDE_BUY", "ORDER_SIDE_SELL"]
OrderIntent = Literal[
    "ORDER_INTENT_BUY_LONG",
    "ORDER_INTENT_SELL_LONG",
    "ORDER_INTENT_BUY_SHORT",
    "ORDER_INTENT_SELL_SHORT",
]
TimeInForce = Literal[
    "TIME_IN_FORCE_GOOD_TILL_CANCEL",
    "TIME_IN_FORCE_GOOD_TILL_DATE",
    "TIME_IN_FORCE_IMMEDIATE_OR_CANCEL",
    "TIME_IN_FORCE_FILL_OR_KILL",
]
OrderState = Literal[
    "ORDER_STATE_NEW",
    "ORDER_STATE_PENDING_NEW",
    "ORDER_STATE_PENDING_REPLACE",
    "ORDER_STATE_PENDING_CANCEL",
    "ORDER_STATE_PENDING_RISK",
    "ORDER_STATE_PARTIALLY_FILLED",
    "ORDER_STATE_FILLED",
    "ORDER_STATE_CANCELED",
    "ORDER_STATE_REPLACED",
    "ORDER_STATE_REJECTED",
    "ORDER_STATE_EXPIRED",
]
ExecutionType = Literal[
    "EXECUTION_TYPE_NEW",
    "EXECUTION_TYPE_PARTIAL_FILL",
    "EXECUTION_TYPE_FILL",
    "EXECUTION_TYPE_CANCELED",
    "EXECUTION_TYPE_REPLACE",
    "EXECUTION_TYPE_REJECTED",
    "EXECUTION_TYPE_EXPIRED",
    "EXECUTION_TYPE_DONE_FOR_DAY",
]
ManualOrderIndicator = Literal[
    "MANUAL_ORDER_INDICATOR_MANUAL",
    "MANUAL_ORDER_INDICATOR_AUTOMATIC",
]


class SlippageTolerance(TypedDict, total=False):
    """Slippage tolerance for market orders."""

    currentPrice: Amount
    bips: int
    ticks: int


class MarketMetadata(TypedDict, total=False):
    """Market metadata included in order responses."""

    slug: str
    icon: str
    title: str
    outcome: str
    eventSlug: str
    teamId: int
    team: dict[str, object]


class Order(TypedDict, total=False):
    """Order details."""

    id: str
    marketSlug: str
    side: OrderSide
    type: OrderType
    price: Amount
    quantity: int
    cumQuantity: int
    leavesQuantity: int
    tif: TimeInForce
    goodTillTime: str
    intent: OrderIntent
    marketMetadata: MarketMetadata
    state: OrderState
    avgPx: Amount
    cashOrderQty: Amount
    insertTime: str
    createTime: str
    commissionNotionalTotalCollected: Amount
    commissionsBasisPoints: str
    makerCommissionsBasisPoints: str


class Execution(TypedDict, total=False):
    """Order execution details."""

    id: str
    order: Order
    lastShares: str
    lastPx: Amount
    type: ExecutionType
    text: str
    orderRejectReason: str
    transactTime: str
    tradeId: str
    aggressor: bool
    commissionNotionalCollected: Amount


class CreateOrderParams(TypedDict, total=False):
    """Parameters for creating an order."""

    marketSlug: str  # Required
    intent: OrderIntent  # Required
    type: OrderType
    price: Amount
    quantity: int
    tif: TimeInForce
    participateDontInitiate: bool
    goodTillTime: str
    cashOrderQty: Amount
    manualOrderIndicator: ManualOrderIndicator
    synchronousExecution: bool
    maxBlockTime: str
    slippageTolerance: SlippageTolerance


class CreateOrderResponse(TypedDict, total=False):
    """Response from creating an order."""

    id: str
    executions: list[Execution]


class ModifyOrderParams(TypedDict, total=False):
    """Parameters for modifying an order."""

    marketSlug: str  # Required
    price: Amount
    quantity: int
    tif: TimeInForce
    participateDontInitiate: bool
    goodTillTime: str


class CancelOrderParams(TypedDict):
    """Parameters for canceling an order."""

    marketSlug: str


class CancelAllOrdersParams(TypedDict, total=False):
    """Parameters for canceling all orders."""

    slugs: list[str]


class CancelAllOrdersResponse(TypedDict):
    """Response from canceling all orders."""

    canceledOrderIds: list[str]


class GetOpenOrdersParams(TypedDict, total=False):
    """Parameters for getting open orders."""

    slugs: list[str]


class GetOpenOrdersResponse(TypedDict):
    """Response for getting open orders."""

    orders: list[Order]


class GetOrderResponse(TypedDict):
    """Response for getting a single order."""

    order: Order


class PreviewOrderParams(TypedDict):
    """Parameters for previewing an order."""

    request: CreateOrderParams


class PreviewOrderResponse(TypedDict):
    """Response from previewing an order."""

    order: Order


class ClosePositionParams(TypedDict, total=False):
    """Parameters for closing a position."""

    marketSlug: str  # Required
    manualOrderIndicator: ManualOrderIndicator
    synchronousExecution: bool
    maxBlockTime: str
    slippageTolerance: SlippageTolerance


class ClosePositionResponse(TypedDict, total=False):
    """Response from closing a position."""

    id: str
    executions: list[Execution]
