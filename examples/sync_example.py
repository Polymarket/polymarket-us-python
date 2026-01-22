"""Synchronous usage example."""

import os

from polymarket_us import PolymarketUS

# Public endpoints (no authentication needed)
client = PolymarketUS()

# List events
print("=== Events ===")
events = client.events.list({"limit": 5, "active": True})
for event in events.get("events", []):
    print(f"- {event.get('title')} (slug: {event.get('slug')})")

# List markets
print("\n=== Markets ===")
markets = client.markets.list({"limit": 5})
for market in markets.get("markets", []):
    print(f"- {market.get('title')} (slug: {market.get('slug')})")

# Search
print("\n=== Search ===")
results = client.search.query({"query": "bitcoin", "limit": 3})
for event in results.get("events", []):
    print(f"- {event.get('title')}")

client.close()

# Authenticated endpoints (requires API keys)
key_id = os.environ.get("POLYMARKET_KEY_ID")
secret_key = os.environ.get("POLYMARKET_SECRET_KEY")

if key_id and secret_key:
    print("\n=== Authenticated Operations ===")
    auth_client = PolymarketUS(key_id=key_id, secret_key=secret_key)

    # Get balances
    balances = auth_client.account.balances()
    print(f"Balances: {balances}")

    # Get positions
    positions = auth_client.portfolio.positions()
    print(f"Positions: {positions}")

    # Get open orders
    orders = auth_client.orders.list()
    print(f"Open orders: {orders}")

    auth_client.close()
else:
    print("\n(Set POLYMARKET_KEY_ID and POLYMARKET_SECRET_KEY to test authenticated endpoints)")
