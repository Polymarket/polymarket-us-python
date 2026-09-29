"""WebSocket usage example."""

import asyncio
import os
from typing import Any

from polymarket_us import PolymarketUS
from polymarket_us.websocket import (
    AccountBalanceSnapshot,
    AccountBalanceUpdate,
    PositionUpdate,
    RFQEvent,
)


async def main() -> None:
    """Run WebSocket example."""
    key_id = os.environ.get("POLYMARKET_KEY_ID")
    secret_key = os.environ.get("POLYMARKET_SECRET_KEY")

    if not key_id or not secret_key:
        print("Set POLYMARKET_KEY_ID and POLYMARKET_SECRET_KEY environment variables")
        return

    client = PolymarketUS(key_id=key_id, secret_key=secret_key)

    # Private WebSocket for orders, positions, balances, and RFQs
    private_ws = client.ws.private()

    def on_order_snapshot(data: dict[str, Any]) -> None:
        orders = data.get("orderSubscriptionSnapshot", {}).get("orders", [])
        print(f"[Private] Order snapshot: {len(orders)} orders")
        for order in orders[:3]:  # Show first 3
            print(f"  - {order.get('id')}: {order.get('state')}")

    def on_order_update(data: dict[str, Any]) -> None:
        execution = data.get("orderSubscriptionUpdate", {}).get("execution", {})
        print(f"[Private] Order update: {execution.get('type')}")

    def on_position_update(data: PositionUpdate) -> None:
        change = data["positionSubscription"]
        print(f"[Private] Position: {change['beforePosition']} -> {change['afterPosition']}")

    def on_balance_snapshot(data: AccountBalanceSnapshot) -> None:
        for balance in data["accountBalancesSnapshot"]["balances"]:
            print(f"[Private] Balance: {balance.get('currentBalance')} {balance.get('currency')}")

    def on_balance_update(data: AccountBalanceUpdate) -> None:
        change = data["accountBalancesUpdate"]["balanceChange"]
        after = change["afterBalance"]
        if after is not None:
            print(f"[Private] Balance: {after.get('currentBalance')} {after.get('currency')}")

    def on_rfq_event(data: RFQEvent) -> None:
        print(f"[Private] RFQ event: {data['rfqEvent']}")

    def on_error(error: Exception) -> None:
        print(f"[Error] {error}")

    def on_heartbeat() -> None:
        print("[Heartbeat]")

    private_ws.on("order_snapshot", on_order_snapshot)
    private_ws.on("order_update", on_order_update)
    private_ws.on("position_update", on_position_update)
    private_ws.on("account_balance_snapshot", on_balance_snapshot)
    private_ws.on("account_balance_update", on_balance_update)
    private_ws.on("rfq_event", on_rfq_event)
    private_ws.on("error", on_error)
    private_ws.on("heartbeat", on_heartbeat)

    print("Connecting to private WebSocket...")
    await private_ws.connect()

    await private_ws.subscribe_orders("orders-1")
    await private_ws.subscribe_positions("positions-1")
    await private_ws.subscribe_account_balance("balance-1")
    await private_ws.subscribe_rfq("rfqs-1")

    # Markets WebSocket for order book and trades
    markets_ws = client.ws.markets()

    def on_market_data(data: dict[str, Any]) -> None:
        market_data = data.get("marketData", {})
        bids = market_data.get("bids", [])
        offers = market_data.get("offers", [])
        print(f"[Market] {market_data.get('marketSlug')}: {len(bids)} bids, {len(offers)} offers")

    def on_market_data_lite(data: dict[str, Any]) -> None:
        lite = data.get("marketDataLite", {})
        print(
            f"[Market Lite] {lite.get('marketSlug')}: "
            f"bid={lite.get('bestBid')}, ask={lite.get('bestAsk')}"
        )

    def on_trade(data: dict[str, Any]) -> None:
        trade = data.get("trade", {})
        print(f"[Trade] {trade.get('marketSlug')}: {trade.get('quantity')} @ {trade.get('price')}")

    markets_ws.on("market_data", on_market_data)
    markets_ws.on("market_data_lite", on_market_data_lite)
    markets_ws.on("trade", on_trade)
    markets_ws.on("error", on_error)

    print("Connecting to markets WebSocket...")
    await markets_ws.connect()

    # Subscribe to a market (replace with a real market slug)
    # await markets_ws.subscribe_market_data("md-1", ["btc-100k-2025"])
    # await markets_ws.subscribe_trades("trades-1", ["btc-100k-2025"])

    print("WebSockets connected. Press Ctrl+C to exit...")

    try:
        # Keep running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

    await private_ws.close()
    await markets_ws.close()
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
