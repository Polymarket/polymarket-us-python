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
        """Create a new order.

        Args:
            params: Order parameters

        Returns:
            Response containing order ID and optional executions
        """
        return self._client.post(
            "/v1/orders",
            body=self._convert_params(dict(params)),
            authenticated=True,
        )

    def list(self, params: GetOpenOrdersParams | None = None) -> GetOpenOrdersResponse:
        """List open orders.

        Args:
            params: Optional filtering parameters

        Returns:
            Response containing list of open orders
        """
        return self._client.get(
            "/v1/orders/open",
            query=self._convert_params(params),
            authenticated=True,
        )

    def retrieve(self, order_id: str) -> GetOrderResponse:
        """Get an order by ID.

        Args:
            order_id: Order ID

        Returns:
            Response containing the order
        """
        return self._client.get(f"/v1/order/{order_id}", authenticated=True)

    def cancel(self, order_id: str, params: CancelOrderParams) -> None:
        """Cancel an order.

        Args:
            order_id: Order ID to cancel
            params: Cancel parameters (requires market_slug)
        """
        self._client.post(
            f"/v1/order/{order_id}/cancel",
            body=self._convert_params(dict(params)),
            authenticated=True,
        )

    def modify(self, order_id: str, params: ModifyOrderParams) -> None:
        """Modify an order.

        Args:
            order_id: Order ID to modify
            params: Modification parameters
        """
        self._client.post(
            f"/v1/order/{order_id}/modify",
            body=self._convert_params(dict(params)),
            authenticated=True,
        )

    def cancel_all(self, params: CancelAllOrdersParams | None = None) -> CancelAllOrdersResponse:
        """Cancel all open orders.

        Args:
            params: Optional parameters to filter which orders to cancel

        Returns:
            Response containing IDs of canceled orders
        """
        return self._client.post(
            "/v1/orders/open/cancel",
            body=self._convert_params(dict(params)) if params else {},
            authenticated=True,
        )

    def preview(self, params: PreviewOrderParams) -> PreviewOrderResponse:
        """Preview an order before creating it.

        Args:
            params: Order parameters to preview

        Returns:
            Response containing the previewed order
        """
        return self._client.post(
            "/v1/order/preview",
            body=self._convert_params(dict(params)),
            authenticated=True,
        )

    def close_position(self, params: ClosePositionParams) -> ClosePositionResponse:
        """Close a position.

        Args:
            params: Close position parameters

        Returns:
            Response containing order ID and optional executions
        """
        return self._client.post(
            "/v1/order/close-position",
            body=self._convert_params(dict(params)),
            authenticated=True,
        )


class AsyncOrders(AsyncAPIResource):
    """Orders API resource (async, requires authentication)."""

    async def create(self, params: CreateOrderParams) -> CreateOrderResponse:
        """Create a new order.

        Args:
            params: Order parameters

        Returns:
            Response containing order ID and optional executions
        """
        return await self._client.post(
            "/v1/orders",
            body=self._convert_params(dict(params)),
            authenticated=True,
        )

    async def list(self, params: GetOpenOrdersParams | None = None) -> GetOpenOrdersResponse:
        """List open orders.

        Args:
            params: Optional filtering parameters

        Returns:
            Response containing list of open orders
        """
        return await self._client.get(
            "/v1/orders/open",
            query=self._convert_params(params),
            authenticated=True,
        )

    async def retrieve(self, order_id: str) -> GetOrderResponse:
        """Get an order by ID.

        Args:
            order_id: Order ID

        Returns:
            Response containing the order
        """
        return await self._client.get(f"/v1/order/{order_id}", authenticated=True)

    async def cancel(self, order_id: str, params: CancelOrderParams) -> None:
        """Cancel an order.

        Args:
            order_id: Order ID to cancel
            params: Cancel parameters (requires market_slug)
        """
        await self._client.post(
            f"/v1/order/{order_id}/cancel",
            body=self._convert_params(dict(params)),
            authenticated=True,
        )

    async def modify(self, order_id: str, params: ModifyOrderParams) -> None:
        """Modify an order.

        Args:
            order_id: Order ID to modify
            params: Modification parameters
        """
        await self._client.post(
            f"/v1/order/{order_id}/modify",
            body=self._convert_params(dict(params)),
            authenticated=True,
        )

    async def cancel_all(
        self, params: CancelAllOrdersParams | None = None
    ) -> CancelAllOrdersResponse:
        """Cancel all open orders.

        Args:
            params: Optional parameters to filter which orders to cancel

        Returns:
            Response containing IDs of canceled orders
        """
        return await self._client.post(
            "/v1/orders/open/cancel",
            body=self._convert_params(dict(params)) if params else {},
            authenticated=True,
        )

    async def preview(self, params: PreviewOrderParams) -> PreviewOrderResponse:
        """Preview an order before creating it.

        Args:
            params: Order parameters to preview

        Returns:
            Response containing the previewed order
        """
        return await self._client.post(
            "/v1/order/preview",
            body=self._convert_params(dict(params)),
            authenticated=True,
        )

    async def close_position(self, params: ClosePositionParams) -> ClosePositionResponse:
        """Close a position.

        Args:
            params: Close position parameters

        Returns:
            Response containing order ID and optional executions
        """
        return await self._client.post(
            "/v1/order/close-position",
            body=self._convert_params(dict(params)),
            authenticated=True,
        )
