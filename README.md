# Polymarket US Python SDK

Official Python SDK for the Polymarket US API.

## Installation

```bash
pip install polymarket-us
```

## Usage

### Public Endpoints (No Authentication)

```python
from polymarket_us import PolymarketUS

client = PolymarketUS()

# Get events with pagination
events = client.events.list({"limit": 10, "offset": 0, "active": True})
next_page = client.events.list({"limit": 10, "offset": 10, "active": True})

# Get a specific event
event = client.events.retrieve(123)
event_by_slug = client.events.retrieve_by_slug("super-bowl-2025")

# Get markets
markets = client.markets.list()
market = client.markets.retrieve_by_slug("btc-100k")

# Get order book
book = client.markets.book("btc-100k")

# Get best bid/offer
bbo = client.markets.bbo("btc-100k")

# Search
results = client.search.query({"query": "bitcoin"})

# Series and sports
series = client.series.list()
sports = client.sports.list()
```

### Authenticated Endpoints (Trading)

```python
import os
from polymarket_us import PolymarketUS

client = PolymarketUS(
    key_id=os.environ["POLYMARKET_KEY_ID"],
    secret_key=os.environ["POLYMARKET_SECRET_KEY"],
)

# Create an order
order = client.orders.create({
    "market_slug": "btc-100k-2025",
    "intent": "ORDER_INTENT_BUY_LONG",
    "type": "ORDER_TYPE_LIMIT",
    "price": {"value": "0.55", "currency": "USD"},
    "quantity": 100,
    "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL",
})

# Get open orders
open_orders = client.orders.list()

# Cancel an order
client.orders.cancel(order["id"], {"market_slug": "btc-100k-2025"})

# Cancel all orders
client.orders.cancel_all()

# Get positions
positions = client.portfolio.positions()

# Get activity history
activities = client.portfolio.activities()

# Get account balances
balances = client.account.balances()

client.close()
```

### Async Usage

```python
import asyncio
import os
from polymarket_us import AsyncPolymarketUS

async def main():
    async with AsyncPolymarketUS(
        key_id=os.environ["POLYMARKET_KEY_ID"],
        secret_key=os.environ["POLYMARKET_SECRET_KEY"],
    ) as client:
        # Concurrent requests
        events, markets = await asyncio.gather(
            client.events.list({"limit": 10}),
            client.markets.list({"limit": 10}),
        )
        print(f"Found {len(events['events'])} events")
        print(f"Found {len(markets['markets'])} markets")

asyncio.run(main())
```

## Authentication

Polymarket US uses Ed25519 signature authentication. Generate API keys at [polymarket.us/developer](https://polymarket.us/developer).

The SDK automatically signs requests with your credentials:

```python
client = PolymarketUS(
    key_id="your-api-key-id",      # UUID
    secret_key="your-secret-key",  # Base64-encoded Ed25519 private key
)
```

## Error Handling

```python
from polymarket_us import (
    PolymarketUS,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
)

try:
    client.orders.create({...})
except AuthenticationError:
    print("Invalid credentials")
except BadRequestError:
    print("Invalid order parameters")
except RateLimitError:
    print("Rate limit exceeded, retry later")
except NotFoundError:
    print("Resource not found")
```

## Configuration

```python
client = PolymarketUS(
    key_id="your-key-id",
    secret_key="your-secret-key",
    timeout=30.0,  # Request timeout in seconds (default: 30.0)
)
```

### WebSocket (Real-Time Data)

```python
import asyncio
import os
from polymarket_us import PolymarketUS

async def main():
    client = PolymarketUS(
        key_id=os.environ["POLYMARKET_KEY_ID"],
        secret_key=os.environ["POLYMARKET_SECRET_KEY"],
    )

    # Private WebSocket (orders, positions, balances)
    private_ws = client.ws.private()

    def on_order_snapshot(data):
        print(f"Open orders: {data['orderSubscriptionSnapshot']['orders']}")

    def on_order_update(data):
        print(f"Order execution: {data['orderSubscriptionUpdate']['execution']}")

    private_ws.on("order_snapshot", on_order_snapshot)
    private_ws.on("order_update", on_order_update)
    private_ws.on("error", lambda e: print(f"Error: {e}"))

    await private_ws.connect()
    await private_ws.subscribe_orders("order-sub-1")
    await private_ws.subscribe_positions("pos-sub-1")
    await private_ws.subscribe_account_balance("balance-sub-1")

    # Markets WebSocket (order book, trades)
    markets_ws = client.ws.markets()

    markets_ws.on("market_data", lambda d: print(f"Book: {d['marketData']}"))
    markets_ws.on("trade", lambda d: print(f"Trade: {d['trade']}"))

    await markets_ws.connect()
    await markets_ws.subscribe_market_data("md-sub-1", ["btc-100k-2025"])
    await markets_ws.subscribe_trades("trade-sub-1", ["btc-100k-2025"])

    # Keep running
    await asyncio.sleep(60)

    await private_ws.close()
    await markets_ws.close()

asyncio.run(main())
```

## API Reference

### Events

| Method | Description |
|--------|-------------|
| `events.list(params?)` | List events with filtering |
| `events.retrieve(id)` | Get event by ID |
| `events.retrieve_by_slug(slug)` | Get event by slug |

### Markets

| Method | Description |
|--------|-------------|
| `markets.list(params?)` | List markets with filtering |
| `markets.retrieve(id)` | Get market by ID |
| `markets.retrieve_by_slug(slug)` | Get market by slug |
| `markets.book(slug)` | Get order book |
| `markets.bbo(slug)` | Get best bid/offer |
| `markets.settlement(slug)` | Get settlement price |

### Orders (Authenticated)

| Method | Description |
|--------|-------------|
| `orders.create(params)` | Create a new order |
| `orders.list(params?)` | Get open orders |
| `orders.retrieve(order_id)` | Get order by ID |
| `orders.cancel(order_id, params)` | Cancel an order |
| `orders.modify(order_id, params)` | Modify an order |
| `orders.cancel_all(params?)` | Cancel all open orders |
| `orders.preview(params)` | Preview an order |
| `orders.close_position(params)` | Close a position |

### Portfolio (Authenticated)

| Method | Description |
|--------|-------------|
| `portfolio.positions(params?)` | Get trading positions |
| `portfolio.activities(params?)` | Get activity history |

### Account (Authenticated)

| Method | Description |
|--------|-------------|
| `account.balances()` | Get account balances |

### Series

| Method | Description |
|--------|-------------|
| `series.list(params?)` | List series |
| `series.retrieve(id)` | Get series by ID |

### Sports

| Method | Description |
|--------|-------------|
| `sports.list()` | List sports |
| `sports.teams(params?)` | Get teams for provider |

### Search

| Method | Description |
|--------|-------------|
| `search.query(params?)` | Search events (includes nested markets) |

### WebSocket (Authenticated)

| Method | Description |
|--------|-------------|
| `ws.private()` | Create private WebSocket connection |
| `ws.markets()` | Create markets WebSocket connection |

**Private WebSocket Events:**
- `order_snapshot` - Initial orders snapshot
- `order_update` - Order execution updates
- `position_snapshot` - Initial positions snapshot
- `position_update` - Position changes
- `account_balance_snapshot` - Initial balance
- `account_balance_update` - Balance changes
- `heartbeat` - Connection keepalive
- `error` - Error events
- `close` - Connection closed

**Markets WebSocket Events:**
- `market_data` - Full order book updates
- `market_data_lite` - Lightweight price data
- `trade` - Trade notifications
- `heartbeat` - Connection keepalive
- `error` - Error events
- `close` - Connection closed

## Requirements

- Python 3.10+

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .

# Run type checking
mypy polymarket_us
```

## License

MIT
