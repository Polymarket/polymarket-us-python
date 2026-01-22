"""Asynchronous usage example."""

import asyncio
import os

from polymarket_us import AsyncPolymarketUS


async def main() -> None:
    """Run async example."""
    # Public endpoints (no authentication needed)
    async with AsyncPolymarketUS() as client:
        # Concurrent requests
        events, markets, series = await asyncio.gather(
            client.events.list({"limit": 5, "active": True}),
            client.markets.list({"limit": 5}),
            client.series.list({"limit": 5}),
        )

        print("=== Events ===")
        for event in events.get("events", []):
            print(f"- {event.get('title')}")

        print("\n=== Markets ===")
        for market in markets.get("markets", []):
            print(f"- {market.get('title')}")

        print("\n=== Series ===")
        for s in series.get("series", []):
            print(f"- {s.get('title')}")

    # Authenticated endpoints (requires API keys)
    key_id = os.environ.get("POLYMARKET_KEY_ID")
    secret_key = os.environ.get("POLYMARKET_SECRET_KEY")

    if key_id and secret_key:
        print("\n=== Authenticated Operations ===")
        async with AsyncPolymarketUS(key_id=key_id, secret_key=secret_key) as auth_client:
            # Concurrent authenticated requests
            balances, positions, orders = await asyncio.gather(
                auth_client.account.balances(),
                auth_client.portfolio.positions(),
                auth_client.orders.list(),
            )

            print(f"Balances: {balances}")
            print(f"Positions: {positions}")
            print(f"Open orders: {orders}")
    else:
        print("\n(Set POLYMARKET_KEY_ID and POLYMARKET_SECRET_KEY to test authenticated endpoints)")


if __name__ == "__main__":
    asyncio.run(main())
