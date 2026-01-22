"""WebSocket usage example."""

import asyncio
import os
from typing import Any

from polymarket_us import PolymarketUS


async def main() -> None:
    """Run WebSocket example."""
    key_id = os.environ.get("POLYMARKET_KEY_ID")
    secret_key = os.environ.get("POLYMARKET_SECRET_KEY")

    if not key_id or not secret_key:
        print("Set POLYMARKET_KEY_ID and POLYMARKET_SECRET_KEY environment variables")
        return

    client = PolymarketUS(key_id=key_id, secret_key=secret_key)

    # Private WebSocket for orders, positions, and balances
    private_ws = client.ws.private()

    def on_order_snapshot(data: dict[str, Any]) -> None:
        orders = data.get("orderSubscriptionSnapshot", {}).get("orders", [])
        print(f"[Private] Order snapshot: {len(orders)} orders")
        for order in orders[:3]:  # Show first 3
            print(f"  - {order.get('id')}: {order.get('state')}")

    def on_order_update(data: dict[str, Any]) -> None:
        execution = data.get("orderSubscriptionUpdate", {}).get("execution", {})
        print(f"[Private] Order update: {execution.get('type')}")

    def on_position_snapshot(data: dict[str, Any]) -> None:
        positions = data.get("positionSubscriptionSnapshot", {}).get("positions", {})
        print(f"[Private] Position snapshot: {len(positions)} positions")

    def on_position_update(data: dict[str, Any]) -> None:
        update = data.get("positionSubscriptionUpdate", {})
        print(f"[Private] Position update: {update.get('marketSlug')}")

    def on_balance_snapshot(data: dict[str, Any]) -> None:
        snapshot = data.get("accountBalanceSubscriptionSnapshot", {})
        print(f"[Private] Balance: ${snapshot.get('balance')}")

    def on_balance_update(data: dict[str, Any]) -> None:
        update = data.get("accountBalanceSubscriptionUpdate", {})
        print(f"[Private] Balance update: ${update.get('balance')}")

    def on_error(error: Exception) -> None:
        print(f"[Error] {error}")

    def on_heartbeat() -> None:
        print("[Heartbeat]")

    private_ws.on("order_snapshot", on_order_snapshot)
    private_ws.on("order_update", on_order_update)
    private_ws.on("position_snapshot", on_position_snapshot)
    private_ws.on("position_update", on_position_update)
    private_ws.on("account_balance_snapshot", on_balance_snapshot)
    private_ws.on("account_balance_update", on_balance_update)
    private_ws.on("error", on_error)
    private_ws.on("heartbeat", on_heartbeat)

    print("Connecting to private WebSocket...")
    await private_ws.connect()

    await private_ws.subscribe_orders("orders-1")
    await private_ws.subscribe_positions("positions-1")
    await private_ws.subscribe_account_balance("balance-1")

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
