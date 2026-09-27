# Trading Engine milestone

## Implemented

- Canonical Order model
- Order side/type/time-in-force/status enums
- Client order ID and broker order ID fields
- Trade execution model
- Order query service
- Order creation service
- Order cancellation service
- Trade-history query
- Deterministic paper broker
- Bid/ask-aware market execution
- Average-cost signed position accounting
- Long-to-short and short-to-long crossing logic
- Realized P&L on closing fills
- Fee accounting
- Cash balance updates
- Portfolio equity recalculation
- Transaction ledger write for each paper fill
- Authenticated order APIs
- Authenticated ownership checks
- Paper execution API

## Paper execution API

Create: `POST /api/trading/orders/{portfolio_id}`

Inspect: `GET /api/trading/orders/{portfolio_id}`

Order: `GET /api/trading/orders/detail/{order_id}`

Trade history: `GET /api/trading/orders/detail/{order_id}/trades`

Cancel: `POST /api/trading/orders/detail/{order_id}/cancel`

Paper execution: `POST /api/trading/orders/detail/{order_id}/paper-execute`

Paper market buys use ask; paper market sells use bid. Last is used only when the relevant side is unavailable.

## Architecture boundary

The strategy layer is not coupled to this API.

```
strategy signal
  -> order intent
  -> risk engine
  -> order
  -> execution venue
  -> trade
  -> transaction
  -> portfolio accounting
```

The paper broker is a development/execution venue. A real broker adapter should implement the same internal contract without exposing broker SDK details to strategy code.

## Not production-ready yet

Before live brokerage:

- deterministic risk engine
- pre-trade validation
- margin/leverage model
- exchange/venue abstraction
- idempotency and duplicate-order protection
- order-event reconciliation
- partial-fill handling
- broker reconnect/replay
- persistent audit log
- broker position reconciliation
- secret management
- production database migrations
- integration tests with a paper adapter
