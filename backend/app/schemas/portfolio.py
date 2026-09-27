from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PortfolioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    cash_balance: float
    equity: float
    buying_power: float
    user_id: int
    created_at: datetime
    updated_at: datetime


class PortfolioValueResponse(BaseModel):
    cash_balance: float
    equity: float
    buying_power: float
