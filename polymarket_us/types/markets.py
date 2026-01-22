"""Markets type definitions."""

from typing import Literal, TypedDict

from polymarket_us.types.common import Amount, PaginationParams


class Team(TypedDict, total=False):
    """Sports team information."""

    id: int
    name: str
    abbreviation: str
    league: str
    record: str
    logo: str
    alias: str
    safe_name: str
    home_icon: str
    away_icon: str
    color_primary: str


class MarketDetail(TypedDict, total=False):
    """Detailed market information."""

    id: int
    slug: str
    title: str
    outcome: str
    description: str
    active: bool
    closed: bool
    liquidity: float
    volume: float
    event_slug: str
    team: Team


class OrderBookLevel(TypedDict):
    """Order book price level."""

    px: Amount
    qty: str


class MarketStats(TypedDict, total=False):
    """Market statistics."""

    last_trade_px: Amount
    shares_traded: str
    open_interest: str
    high_px: Amount
    low_px: Amount


MarketState = Literal[
    "MARKET_STATE_OPEN",
    "MARKET_STATE_PREOPEN",
    "MARKET_STATE_SUSPENDED",
    "MARKET_STATE_HALTED",
    "MARKET_STATE_EXPIRED",
    "MARKET_STATE_TERMINATED",
    "MARKET_STATE_MATCH_AND_CLOSE_AUCTION",
]


class MarketBook(TypedDict, total=False):
    """Order book for a market."""

    market_slug: str
    bids: list[OrderBookLevel]
    offers: list[OrderBookLevel]
    state: MarketState
    stats: MarketStats
    transact_time: str


class MarketBBO(TypedDict, total=False):
    """Best bid/offer for a market."""

    market_slug: str
    best_bid: Amount
    best_ask: Amount
    bid_depth: int
    ask_depth: int
    last_trade_px: Amount
    shares_traded: str
    open_interest: str


class MarketSettlement(TypedDict):
    """Market settlement information."""

    market_slug: str
    settlement_price: Amount
    settled_at: str


class MarketsListParams(PaginationParams, total=False):
    """Parameters for listing markets."""

    order_by: list[str]
    order_direction: Literal["asc", "desc"]
    id: list[int]
    slug: list[str]
    event_slug: list[str]
    archived: bool
    active: bool
    closed: bool
    liquidity_min: float
    liquidity_max: float
    volume_min: float
    volume_max: float
    game_id: int
    categories: list[str]


class GetMarketsResponse(TypedDict):
    """Response for listing markets."""

    markets: list[MarketDetail]


class GetMarketResponse(TypedDict):
    """Response for getting a single market."""

    market: MarketDetail
