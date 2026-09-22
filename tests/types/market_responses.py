"""Consumer typing checks included in the existing mypy CI job."""

from polymarket_us import AsyncPolymarketUS, PolymarketUS
from polymarket_us.types import (
    GetMarketBBOResponse,
    GetMarketBookResponse,
    MarketBBO,
    MarketBook,
)


def read_market_data(client: PolymarketUS) -> tuple[MarketBook, MarketBBO, str, float]:
    book = client.markets.book("market")
    bbo = client.markets.bbo("market")
    settlement = client.markets.settlement("market")
    return book["marketData"], bbo["marketData"], settlement["slug"], settlement["settlement"]


async def read_market_data_async(
    client: AsyncPolymarketUS,
) -> tuple[MarketBook, MarketBBO, str, float]:
    book = await client.markets.book("market")
    bbo = await client.markets.bbo("market")
    settlement = await client.markets.settlement("market")
    return book["marketData"], bbo["marketData"], settlement["slug"], settlement["settlement"]


empty_book: GetMarketBookResponse = {
    "marketData": {
        "marketSlug": "market",
        "bids": [],
        "offers": [],
        "state": "MARKET_STATE_CLOSED",
        "stats": None,
        "transactTime": None,
    }
}

empty_bbo: GetMarketBBOResponse = {
    "marketData": {
        "marketSlug": "market",
        "bestBid": None,
        "bestAsk": None,
        "lastTradePx": None,
        "bidDepth": 0,
        "askDepth": 0,
        "sharesTraded": "",
        "openInterest": "",
    }
}
