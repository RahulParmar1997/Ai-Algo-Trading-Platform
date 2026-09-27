from pydantic import BaseModel, ConfigDict, computed_field


class PositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol: str
    quantity: int
    average_price: float
    current_price: float
    portfolio_id: int

    @computed_field
    @property
    def market_value(self) -> float:
        return self.quantity * self.current_price

    @computed_field
    @property
    def unrealized_pnl(self) -> float:
        return (self.current_price - self.average_price) * self.quantity
