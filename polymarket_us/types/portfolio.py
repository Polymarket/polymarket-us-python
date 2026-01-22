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

    netPosition: str
    qtyBought: str
    qtySold: str
    cost: Amount
    realized: Amount
    bodPosition: str
    expired: bool
    updateTime: str
    marketMetadata: MarketMetadata
    cashValue: Amount
    qtyAvailable: str


class GetUserPositionsParams(TypedDict, total=False):
    """Parameters for getting user positions."""

    market: str
    limit: int
    cursor: str


class GetUserPositionsResponse(TypedDict, total=False):
    """Response for getting user positions."""

    positions: dict[str, UserPosition]
    nextCursor: str
    eof: bool


class Trade(TypedDict, total=False):
    """Trade details."""

    id: str
    marketSlug: str
    state: str
    createTime: str
    updateTime: str
    price: Amount
    qty: str
    isAggressor: bool
    costBasis: Amount
    realizedPnl: Amount


class PositionResolution(TypedDict, total=False):
    """Position resolution details."""

    marketSlug: str
    beforePosition: UserPosition
    afterPosition: UserPosition
    updateTime: str
    tradeId: str
    side: str


class AccountBalanceChangeTransaction(TypedDict, total=False):
    """Account balance change transaction."""

    transactionId: str
    status: str
    amount: Amount
    updateTime: str
    createTime: str


class AccountBalanceChange(TypedDict, total=False):
    """Account balance change."""

    transactions: list[AccountBalanceChangeTransaction]


class Activity(TypedDict, total=False):
    """Activity record."""

    type: ActivityType
    trade: Trade
    positionResolution: PositionResolution
    accountBalanceChange: AccountBalanceChange


class GetActivitiesParams(TypedDict, total=False):
    """Parameters for getting activities."""

    limit: int
    cursor: str
    marketSlug: str
    types: list[ActivityType]
    sortOrder: SortOrder


class GetActivitiesResponse(TypedDict, total=False):
    """Response for getting activities."""

    activities: list[Activity]
    nextCursor: str
    eof: bool
