"""Consumer checks for batch requests, exported types, and sync/async responses."""

from polymarket_us import AsyncPolymarketUS, PolymarketUS
from polymarket_us.types import (
    CancelOrderListItem,
    CancelOrderListParams,
    CancelOrderListResponse,
    CancelOrderParams,
    CreateOrderListParams,
    CreateOrderListResponse,
    CreateOrderParams,
    ModifyOrderListItem,
    ModifyOrderListParams,
    ModifyOrderListResponse,
    ModifyOrderParams,
)

create_order: CreateOrderParams = {
    "marketSlug": "market-a",
    "intent": "ORDER_INTENT_BUY_LONG",
    "price": {"value": "0.50", "currency": "USD"},
    "quantity": 1.25,
}
cancel_order: CancelOrderParams = {"marketSlug": "market-a"}
modify_order: ModifyOrderParams = {
    "marketSlug": "market-a",
    "price": {"value": "0.55", "currency": "USD"},
    "quantity": 1.25,
}
cancel_item: CancelOrderListItem = {**cancel_order, "orderId": "order-a"}
modify_item: ModifyOrderListItem = {**modify_order, "orderId": "order-a"}
create: CreateOrderListParams = {"orders": [create_order, {**create_order, "quantity": 10}]}
cancel: CancelOrderListParams = {"orders": [cancel_item]}
modify: ModifyOrderListParams = {"orders": [modify_item, {**modify_item, "quantity": 5}]}


def batches(client: PolymarketUS) -> tuple[list[str], list[str], list[str]]:
    created: CreateOrderListResponse = client.orders.create_many(create)
    canceled: CancelOrderListResponse = client.orders.cancel_many(cancel)
    modified: ModifyOrderListResponse = client.orders.modify_many(modify)
    return created["createdOrderIds"], canceled["canceledOrderIds"], modified["modifiedOrderIds"]


async def async_batches(client: AsyncPolymarketUS) -> tuple[list[str], list[str], list[str]]:
    created: CreateOrderListResponse = await client.orders.create_many(create)
    canceled: CancelOrderListResponse = await client.orders.cancel_many(cancel)
    modified: ModifyOrderListResponse = await client.orders.modify_many(modify)
    return created["createdOrderIds"], canceled["canceledOrderIds"], modified["modifiedOrderIds"]
