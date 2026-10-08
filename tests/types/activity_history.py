"""Typed consumers of activity time filters and reward categories."""

from polymarket_us import AsyncPolymarketUS, PolymarketUS
from polymarket_us.types import Activity, ActivityType, GetActivitiesParams, GetActivitiesResponse

reward_types: list[ActivityType] = [
    "ACTIVITY_TYPE_TAKER_FEE_REBATE",
    "ACTIVITY_TYPE_LIQUIDITY_PROGRAM",
]
params: GetActivitiesParams = {
    "startTime": "2026-10-01T00:00:00.123456789Z",
    "endTime": "2026-10-02T00:00:00.123456789+00:00",
    "types": reward_types,
    "limit": 2,
    "cursor": "opaque+/=cursor",
    "marketSlug": "example-market",
    "sortOrder": "SORT_ORDER_ASCENDING",
}
activities: list[Activity] = [{"type": value} for value in reward_types]


def history(client: PolymarketUS) -> GetActivitiesResponse:
    return client.portfolio.activities(params)


async def async_history(client: AsyncPolymarketUS) -> GetActivitiesResponse:
    return await client.portfolio.activities(params)
