# Backend

FastAPI backend foundation for the AI Algo Trading Platform.

## Architecture

- API: HTTP/WebSocket endpoints
- Services: application/domain operations
- Engine: event-driven trading components
- Adapters: brokers/exchanges
- Models: persistence
- Schemas: API contracts

Roadmap:

1. Portfolio
2. Trading
3. Market
4. AI Advisor
5. News and remaining admin capabilities

## Local development

Python 3.12+ is recommended.

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Health:

```
GET /health
```

Auth:

```
POST /auth/register
POST /auth/login
GET  /auth/me
```

Portfolio:

```
GET /api/portfolios/{portfolio_id}
GET /api/portfolios/{portfolio_id}/value
GET /api/portfolios/{portfolio_id}/positions
GET /api/portfolios/{portfolio_id}/analytics
GET /api/portfolios/{portfolio_id}/transactions
GET /api/portfolios/{portfolio_id}/performance
```

Trading:

```
POST /api/trading/orders/{portfolio_id}
GET  /api/trading/orders/{portfolio_id}
GET  /api/trading/orders/detail/{order_id}
POST /api/trading/orders/detail/{order_id}/cancel
POST /api/trading/orders/detail/{order_id}/paper-execute
```

For paper market orders, buy fills use the supplied ask and sell fills use the supplied bid; last is a fallback when the corresponding side is unavailable. Live broker integration will use broker-native quotes and adapters instead.

Set `SECRET_KEY` in `.env` before any non-development deployment.

## Design rule

Strategy code must never call a broker directly. The intended live path is:

market data -> features/signals -> decision -> risk -> order plan -> broker adapter -> broker
