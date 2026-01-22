"""Portfolio type definitions."""

from typing import Literal, TypedDict

from polymarket_us.types.common import Amount
from polymarket_us.types.orders import MarketMetadata

ActivityType = Literal[
    "ACTIVITY_TYPE_TRADE",
    "ACTIVITY_TYPE_POSITION_RESOLUTION",
    "ACTIVITY_TYPE_ACCOUNT_DEPOSIT",
    "ACTIVITY_TYPE_ACCOUNT_ADVANCED_DEPOSIT",
    "ACTIVITY_TYPE_ACCOUNT_WITHDRAWAL",
    "ACTIVITY_TYPE_REFERRAL_BONUS",
    "ACTIVITY_TYPE_TRANSFER",
]

SortOrder = Literal["SORT_ORDER_DESCENDING", "SORT_ORDER_ASCENDING"]


class UserPosition(TypedDict, total=False):
    """User position details."""

    net_position: str
    qty_bought: str
    qty_sold: str
    cost: Amount
    realized: Amount
    bod_position: str
    expired: bool
    update_time: str
    market_metadata: MarketMetadata
    cash_value: Amount
    qty_available: str


class GetUserPositionsParams(TypedDict, total=False):
    """Parameters for getting user positions."""

    market: str
    limit: int
    cursor: str


class GetUserPositionsResponse(TypedDict, total=False):
    """Response for getting user positions."""

    positions: dict[str, UserPosition]
    next_cursor: str
    eof: bool


class Trade(TypedDict, total=False):
    """Trade details."""

    id: str
    market_slug: str
    state: str
    create_time: str
    update_time: str
    price: Amount
    qty: str
    is_aggressor: bool
    cost_basis: Amount
    realized_pnl: Amount


class PositionResolution(TypedDict, total=False):
    """Position resolution details."""

    market_slug: str
    before_position: UserPosition
    after_position: UserPosition
    update_time: str
    trade_id: str
    side: str


class AccountBalanceChangeTransaction(TypedDict, total=False):
    """Account balance change transaction."""

    transaction_id: str
    status: str
    amount: Amount
    update_time: str
    create_time: str


class AccountBalanceChange(TypedDict, total=False):
    """Account balance change."""

    transactions: list[AccountBalanceChangeTransaction]


class Activity(TypedDict, total=False):
    """Activity record."""

    type: ActivityType
    trade: Trade
    position_resolution: PositionResolution
    account_balance_change: AccountBalanceChange


class GetActivitiesParams(TypedDict, total=False):
    """Parameters for getting activities."""

    limit: int
    cursor: str
    market_slug: str
    types: list[ActivityType]
    sort_order: SortOrder


class GetActivitiesResponse(TypedDict, total=False):
    """Response for getting activities."""

    activities: list[Activity]
    next_cursor: str
    eof: bool
