"""Batch order contracts through the real HTTP clients and signing path."""

import base64
import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

import httpx
import pytest
from nacl.signing import SigningKey
from pytest_httpx import HTTPXMock

from polymarket_us import (
    APIStatusError,
    APITimeoutError,
    AsyncPolymarketUS,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    PolymarketUS,
    RateLimitError,
)
from polymarket_us.types import (
    CancelOrderListParams,
    CreateOrderListParams,
    ModifyOrderListParams,
)

TEST_SECRET_KEY = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="
pytestmark = pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])


@dataclass
class BatchCase:
    path: str
    body: object
    response: dict[str, list[str]]
    sync_call: Callable[[PolymarketUS], object]
    async_call: Callable[[AsyncPolymarketUS], Awaitable[object]]


def batch_cases(count: int = 2) -> list[BatchCase]:
    create: CreateOrderListParams = {
        "orders": [
            {
                "marketSlug": f"market-{i}",
                "intent": "ORDER_INTENT_BUY_LONG",
                "type": "ORDER_TYPE_LIMIT",
                "price": {"value": "0.1234", "currency": "USD"},
                "quantity": 1.25 if i == 0 else i + 1,
                "tif": "TIME_IN_FORCE_GOOD_TILL_DATE",
                "goodTillTime": "2027-01-01T00:00:00Z",
                "participateDontInitiate": True,
                "manualOrderIndicator": "MANUAL_ORDER_INDICATOR_AUTOMATIC",
                "synchronousExecution": True,
                "maxBlockTime": "1",
                "slippageTolerance": {"bips": 10},
            }
            for i in range(count)
        ]
    }
    cancel: CancelOrderListParams = {
        "orders": [{"orderId": f"order-{i}", "marketSlug": f"market-{i}"} for i in range(count)]
    }
    modify: ModifyOrderListParams = {
        "orders": [
            {
                "orderId": f"order-{i}",
                "marketSlug": f"market-{i}",
                "price": {"value": "0.4321", "currency": "USD"},
                "quantity": 1.25 if i == 0 else i + 1,
                "tif": "TIME_IN_FORCE_GOOD_TILL_DATE",
                "goodTillTime": "2027-01-01T00:00:00Z",
                "participateDontInitiate": False,
            }
            for i in range(count)
        ]
    }
    return [
        BatchCase(
            "/v1/orders/batched",
            create,
            {"createdOrderIds": ["created-b", "created-a"]},
            lambda client: client.orders.create_many(create),
            lambda client: client.orders.create_many(create),
        ),
        BatchCase(
            "/v1/orders/batched/cancel",
            cancel,
            {"canceledOrderIds": ["order-1", "order-0"]},
            lambda client: client.orders.cancel_many(cancel),
            lambda client: client.orders.cancel_many(cancel),
        ),
        BatchCase(
            "/v1/orders/batched/modify",
            modify,
            {"modifiedOrderIds": ["order-1", "order-0"]},
            lambda client: client.orders.modify_many(modify),
            lambda client: client.orders.modify_many(modify),
        ),
    ]


async def invoke(case: BatchCase, asynchronous: bool, authenticated: bool = True) -> object:
    key_id = "test-key" if authenticated else None
    secret_key = TEST_SECRET_KEY if authenticated else None
    if asynchronous:
        async with AsyncPolymarketUS(
            key_id=key_id, secret_key=secret_key, api_base_url="https://api.test", max_retries=3
        ) as client:
            return await case.async_call(client)
    with PolymarketUS(
        key_id=key_id, secret_key=secret_key, api_base_url="https://api.test", max_retries=3
    ) as sync_client:
        return case.sync_call(sync_client)


@pytest.mark.parametrize("case", batch_cases(), ids=["create", "cancel", "modify"])
async def test_batch_request_and_response(
    case: BatchCase, asynchronous: bool, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(json=case.response)

    assert await invoke(case, asynchronous) == case.response

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "POST"
    assert str(request.url) == f"https://api.test{case.path}"
    assert json.loads(request.content) == case.body
    assert request.headers["Content-Type"] == "application/json"
    assert request.headers["X-PM-Access-Key"] == "test-key"
    message = f"{request.headers['X-PM-Timestamp']}POST{case.path}".encode()
    verify_key = SigningKey(base64.b64decode(TEST_SECRET_KEY)).verify_key
    verify_key.verify(message, base64.b64decode(request.headers["X-PM-Signature"]))


@pytest.mark.parametrize("case", batch_cases(), ids=["create", "cancel", "modify"])
@pytest.mark.parametrize(
    ("status", "error_type"),
    [(400, BadRequestError), (429, RateLimitError), (503, InternalServerError)],
)
async def test_batch_errors_are_preserved_without_retry(
    case: BatchCase,
    asynchronous: bool,
    status: int,
    error_type: type[APIStatusError],
    httpx_mock: HTTPXMock,
) -> None:
    payload = {"code": status, "message": "batch rejected"}
    httpx_mock.add_response(status_code=status, json=payload, headers={"Retry-After": "0"})

    with pytest.raises(error_type, match="batch rejected") as exc:
        await invoke(case, asynchronous)

    assert exc.value.status_code == status
    assert exc.value.body == payload
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert exc.value.request_id == requests[0].headers["poly-correlation-id"]


@pytest.mark.parametrize("case", batch_cases(), ids=["create", "cancel", "modify"])
async def test_batch_timeout_is_not_retried(
    case: BatchCase, asynchronous: bool, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_exception(httpx.ReadTimeout("response lost after submission"))

    with pytest.raises(APITimeoutError):
        await invoke(case, asynchronous)

    assert len(httpx_mock.get_requests()) == 1


@pytest.mark.parametrize("case", batch_cases(), ids=["create", "cancel", "modify"])
async def test_batch_requires_credentials_before_sending(
    case: BatchCase, asynchronous: bool, httpx_mock: HTTPXMock
) -> None:
    with pytest.raises(AuthenticationError):
        await invoke(case, asynchronous, authenticated=False)

    assert httpx_mock.get_requests() == []


@pytest.mark.parametrize("case", [*batch_cases(0), *batch_cases(21)])
async def test_batch_size_validation_is_left_to_server(
    case: BatchCase, asynchronous: bool, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(status_code=400, json={"message": "invalid batch size"})

    with pytest.raises(BadRequestError, match="invalid batch size"):
        await invoke(case, asynchronous)

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert json.loads(requests[0].content) == case.body
