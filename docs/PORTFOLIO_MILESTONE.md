# Portfolio milestone

Implemented in the backend foundation:

- SQLAlchemy User, Portfolio and Position models
- Portfolio service with eager-loaded positions
- `GET /api/portfolios/{portfolio_id}`
- `GET /api/portfolios/{portfolio_id}/value`
- `GET /api/portfolios/{portfolio_id}/positions`
- FastAPI lifespan-based database initialization
- Basic API smoke test

## Authentication boundary

These development routes currently address portfolios by ID. Before exposing them to end users, wrap them with the project's JWT/current-user dependency and enforce portfolio ownership at the query level.

## Next portfolio work

- portfolio creation
- default portfolio provisioning after registration
- transaction ledger
- realized/unrealized P&L
- allocation/exposure calculations
- portfolio performance time series
- broker-synced positions
- pagination and filtering
