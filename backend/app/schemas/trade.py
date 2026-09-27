from datetime import datetime

from pydantic import BaseModel


class TradeResponse(BaseModel):
    id: int
    order_id: int
    portfolio_id: int
    symbol: str
    side: str
    quantity: int
    price: float
    fees: float
    executed_at: datetime
    execution_id: str | None

    model_config = {"from_attributes": True}
