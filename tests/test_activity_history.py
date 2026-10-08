"""Activity filters pass through both clients without losing timestamp or type values."""

from copy import deepcopy

import pytest
from pytest_httpx import HTTPXMock

from polymarket_us import AsyncPolymarketUS, PolymarketUS
from polymarket_us.types import GetActivitiesParams, GetActivitiesResponse
from tests.types.activity_history import activities, params

TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="

QUERIES: list[GetActivitiesParams | None] = [
    None,
    {
        "startTime": "2026-10-01T00:00:00.123456789Z",
        "types": ["ACTIVITY_TYPE_TAKER_FEE_REBATE"],
    },
    {
        "endTime": "2026-10-02T00:00:00.123456789+05:30",
        "types": ["ACTIVITY_TYPE_LIQUIDITY_PROGRAM"],
    },
    params,
]


@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("query", QUERIES, ids=["omitted", "start-only", "end-only", "combined"])
async def test_activity_history_filters(
    httpx_mock: HTTPXMock, asynchronous: bool, query: GetActivitiesParams | None
) -> None:
    response: GetActivitiesResponse = {
        "activities": activities,
        "nextCursor": "next+/=cursor",
        "eof": False,
    }
    httpx_mock.add_response(json=response)
    original_query = deepcopy(query)

    if asynchronous:
        async with AsyncPolymarketUS(
            key_id="offline", secret_key=TEST_SECRET_KEY, api_base_url="https://api.test"
        ) as client:
            result = await client.portfolio.activities(query)
    else:
        with PolymarketUS(
            key_id="offline", secret_key=TEST_SECRET_KEY, api_base_url="https://api.test"
        ) as sync_client:
            result = sync_client.portfolio.activities(query)

    assert result == response
    assert query == original_query
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "GET"
    assert request.url.host == "api.test"
    assert request.url.path == "/v1/portfolio/activities"
    assert request.content == b""
    assert request.headers["X-PM-Access-Key"] == "offline"
    expected = original_query or {}
    assert set(request.url.params) == set(expected)
    for key, value in expected.items():
        assert request.url.params.get_list(key) == (
            value if isinstance(value, list) else [str(value)]
        )
