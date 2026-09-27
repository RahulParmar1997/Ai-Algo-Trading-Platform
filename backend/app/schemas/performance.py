from datetime import datetime

from pydantic import BaseModel


class AllocationItem(BaseModel):
    symbol: str
    quantity: int
    market_value: float
    allocation_pct: float
    unrealized_pnl: float


class PortfolioAnalyticsResponse(BaseModel):
    portfolio_id: int
    cash_balance: float
    equity: float
    buying_power: float
    market_value: float
    gross_exposure: float
    net_exposure: float
    gross_exposure_pct: float
    realized_pnl: float
    unrealized_pnl: float
    total_fees: float
    net_pnl: float
    return_pct: float
    invested_pct: float
    allocation: list[AllocationItem]


class PortfolioSnapshotResponse(BaseModel):
    id: int
    portfolio_id: int
    captured_at: datetime
    cash_balance: float
    market_value: float
    equity: float
    daily_return: float
    cumulative_return: float
    drawdown: float
