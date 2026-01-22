"""Orders resource."""

from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import (
    CancelAllOrdersParams,
    CancelAllOrdersResponse,
    CancelOrderParams,
    ClosePositionParams,
    ClosePositionResponse,
    CreateOrderParams,
    CreateOrderResponse,
    GetOpenOrdersParams,
    GetOpenOrdersResponse,
    GetOrderResponse,
    ModifyOrderParams,
    PreviewOrderParams,
    PreviewOrderResponse,
)


class Orders(APIResource):
    """Orders API resource (requires authentication)."""

    def create(self, params: CreateOrderParams) -> CreateOrderResponse:
        """Create a new order."""
        return self._client.post(
            "/v1/orders",
            body=dict(params),
            authenticated=True,
        )

    def list(self, params: GetOpenOrdersParams | None = None) -> GetOpenOrdersResponse:
        """List open orders."""
        return self._client.get(
            "/v1/orders/open",
            query=dict(params) if params else None,
            authenticated=True,
        )

    def retrieve(self, order_id: str) -> GetOrderResponse:
        """Get an order by ID."""
        return self._client.get(f"/v1/order/{order_id}", authenticated=True)

    def cancel(self, order_id: str, params: CancelOrderParams) -> None:
        """Cancel an order."""
        self._client.post(
            f"/v1/order/{order_id}/cancel",
            body=dict(params),
            authenticated=True,
        )

    def modify(self, order_id: str, params: ModifyOrderParams) -> None:
        """Modify an order."""
        self._client.post(
            f"/v1/order/{order_id}/modify",
            body=dict(params),
            authenticated=True,
        )

    def cancel_all(self, params: CancelAllOrdersParams | None = None) -> CancelAllOrdersResponse:
        """Cancel all open orders."""
        return self._client.post(
            "/v1/orders/open/cancel",
            body=dict(params) if params else {},
            authenticated=True,
        )

    def preview(self, params: PreviewOrderParams) -> PreviewOrderResponse:
        """Preview an order before creating it."""
        return self._client.post(
            "/v1/order/preview",
            body=dict(params),
            authenticated=True,
        )

    def close_position(self, params: ClosePositionParams) -> ClosePositionResponse:
        """Close a position."""
        return self._client.post(
            "/v1/order/close-position",
            body=dict(params),
            authenticated=True,
        )


class AsyncOrders(AsyncAPIResource):
    """Orders API resource (async, requires authentication)."""

    async def create(self, params: CreateOrderParams) -> CreateOrderResponse:
        """Create a new order."""
        return await self._client.post(
            "/v1/orders",
            body=dict(params),
            authenticated=True,
        )

    async def list(self, params: GetOpenOrdersParams | None = None) -> GetOpenOrdersResponse:
        """List open orders."""
        return await self._client.get(
            "/v1/orders/open",
            query=dict(params) if params else None,
            authenticated=True,
        )

    async def retrieve(self, order_id: str) -> GetOrderResponse:
        """Get an order by ID."""
        return await self._client.get(f"/v1/order/{order_id}", authenticated=True)

    async def cancel(self, order_id: str, params: CancelOrderParams) -> None:
        """Cancel an order."""
        await self._client.post(
            f"/v1/order/{order_id}/cancel",
            body=dict(params),
            authenticated=True,
        )

    async def modify(self, order_id: str, params: ModifyOrderParams) -> None:
        """Modify an order."""
        await self._client.post(
            f"/v1/order/{order_id}/modify",
            body=dict(params),
            authenticated=True,
        )

    async def cancel_all(
        self, params: CancelAllOrdersParams | None = None
    ) -> CancelAllOrdersResponse:
        """Cancel all open orders."""
        return await self._client.post(
            "/v1/orders/open/cancel",
            body=dict(params) if params else {},
            authenticated=True,
        )

    async def preview(self, params: PreviewOrderParams) -> PreviewOrderResponse:
        """Preview an order before creating it."""
        return await self._client.post(
            "/v1/order/preview",
            body=dict(params),
            authenticated=True,
        )

    async def close_position(self, params: ClosePositionParams) -> ClosePositionResponse:
        """Close a position."""
        return await self._client.post(
            "/v1/order/close-position",
            body=dict(params),
            authenticated=True,
        )
