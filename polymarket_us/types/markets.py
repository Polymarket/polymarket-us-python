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
    safeName: str
    homeIcon: str
    awayIcon: str
    colorPrimary: str


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
    eventSlug: str
    team: Team


class OrderBookLevel(TypedDict):
    """Order book price level."""

    px: Amount
    qty: str


class MarketStats(TypedDict, total=False):
    """Market statistics."""

    lastTradePx: Amount
    sharesTraded: str
    openInterest: str
    highPx: Amount
    lowPx: Amount


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

    marketSlug: str
    bids: list[OrderBookLevel]
    offers: list[OrderBookLevel]
    state: MarketState
    stats: MarketStats
    transactTime: str


class MarketBBO(TypedDict, total=False):
    """Best bid/offer for a market."""

    marketSlug: str
    bestBid: Amount
    bestAsk: Amount
    bidDepth: int
    askDepth: int
    lastTradePx: Amount
    sharesTraded: str
    openInterest: str


class MarketSettlement(TypedDict):
    """Market settlement information."""

    marketSlug: str
    settlementPrice: Amount
    settledAt: str


class MarketsListParams(PaginationParams, total=False):
    """Parameters for listing markets."""

    orderBy: list[str]
    orderDirection: Literal["asc", "desc"]
    id: list[int]
    slug: list[str]
    eventSlug: list[str]
    archived: bool
    active: bool
    closed: bool
    liquidityMin: float
    liquidityMax: float
    volumeMin: float
    volumeMax: float
    gameId: int
    categories: list[str]


class GetMarketsResponse(TypedDict):
    """Response for listing markets."""

    markets: list[MarketDetail]


class GetMarketResponse(TypedDict):
    """Response for getting a single market."""

    market: MarketDetail
