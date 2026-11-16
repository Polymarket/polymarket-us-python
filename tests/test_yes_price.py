"""Confirmation is opt-in and preserves YES prices through both HTTP clients."""

import base64
import json

import pytest
from pytest_httpx import HTTPXMock

from polymarket_us import AsyncPolymarketUS, PolymarketUS
from polymarket_us.types import CreateOrderParams, ModifyOrderParams


@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("confirmation", [None, False, True])
async def test_yes_price_confirmation_wire_contract(
    asynchronous: bool, confirmation: bool | None, httpx_mock: HTTPXMock
) -> None:
    create: CreateOrderParams = {
        "marketSlug": "test",
        "intent": "ORDER_INTENT_BUY_SHORT",
        "price": {"value": "0.95", "currency": "USD"},
    }
    modify: ModifyOrderParams = {"marketSlug": "test", "price": create["price"]}
    if confirmation is not None:
        create["priceIsYes"] = confirmation
        modify["priceIsYes"] = confirmation
    cases = [
        ("create", "/v1/orders", create),
        ("modify", "/v1/order/original/modify", modify),
        ("preview", "/v1/order/preview", {"request": create}),
        ("create_many", "/v1/orders/batched", {"orders": [create]}),
        (
            "modify_many",
            "/v1/orders/batched/modify",
            {"orders": [{**modify, "orderId": "original"}]},
        ),
    ]
    credentials = {"key_id": "test", "secret_key": base64.b64encode(bytes(range(32))).decode()}
    for operation, path, body in cases:
        httpx_mock.add_response(json={})
        args = ("original", body) if operation == "modify" else (body,)
        if asynchronous:
            async with AsyncPolymarketUS(**credentials) as client:
                await getattr(client.orders, operation)(*args)
        else:
            with PolymarketUS(**credentials) as sync_client:
                getattr(sync_client.orders, operation)(*args)
        request = httpx_mock.get_requests()[-1]
        assert request.method == "POST"
        assert request.url.path == path
        assert json.loads(request.content) == body
