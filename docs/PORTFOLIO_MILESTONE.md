# Portfolio milestone

## Phase 1 — foundation

- SQLAlchemy User, Portfolio and Position models
- Portfolio service with eager-loaded positions
- Portfolio value and positions APIs
- Authenticated portfolio ownership enforcement
- JWT authentication and automatic Main Portfolio provisioning

## Phase 2 — analytics

- Immutable-style transaction ledger model
- Portfolio performance snapshot model
- Portfolio analytics service
- Realized P&L aggregation from ledger
- Unrealized P&L from current positions
- Fee aggregation
- Gross exposure and net exposure
- Allocation by symbol
- Return percentage
- Transaction history API with pagination
- Performance snapshot history API with pagination
- Internal snapshot recorder for future scheduled/event-driven use

## APIs

Authentication:

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

Portfolio:

- `GET /api/portfolios/{portfolio_id}`
- `GET /api/portfolios/{portfolio_id}/value`
- `GET /api/portfolios/{portfolio_id}/positions`
- `GET /api/portfolios/{portfolio_id}/analytics`
- `GET /api/portfolios/{portfolio_id}/transactions?limit=100&offset=0`
- `GET /api/portfolios/{portfolio_id}/performance?limit=365&offset=0`

## Data semantics

Transaction `realized_pnl` is treated as the gross realized P&L recorded by the execution/trading layer. Portfolio analytics subtracts ledger fees separately.

For long/short portfolios:

- net exposure = signed market value
- gross exposure = sum of absolute position market values
- allocation remains signed by market value
- gross exposure percentage is gross exposure divided by equity

## Next portfolio work

Before entering the full Trading Engine, add:

- transaction write service used by paper/live execution
- deterministic cost basis handling
- cash/equity reconciliation
- daily/accounting close
- portfolio performance jobs
- broker position reconciliation
- Alembic migrations for production schema management
