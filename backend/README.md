# Backend

FastAPI backend foundation for the AI Algo Trading Platform.

## Architecture

The backend is organized around stable domain interfaces:

- API: HTTP/WebSocket endpoints
- Services: application/domain operations
- Engine: event-driven trading components
- Adapters: brokers/exchanges
- Models: persistence
- Schemas: API contracts

The product roadmap is preserved as:

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
pip install -e .
uvicorn app.main:app --reload
```

Health endpoint:

```
GET /health
```

Portfolio endpoints are intentionally small in this foundation and will expand as the portfolio domain is completed.

## Design rule

Strategy code must never call a broker directly. The intended live path is:

market data -> features/signals -> decision -> risk -> order plan -> broker adapter
