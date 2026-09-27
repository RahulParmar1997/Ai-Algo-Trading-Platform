from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.transaction import TransactionSide


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    portfolio_id: int
    symbol: str | None
    side: TransactionSide
    quantity: int
    price: float
    fees: float
    realized_pnl: float
    cash_delta: float
    reference: str | None
    occurred_at: datetime
