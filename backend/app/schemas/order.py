from datetime import datetime

from pydantic import BaseModel, Field

from app.models.order import OrderSide, OrderStatus, OrderType, TimeInForce


class OrderCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    side: OrderSide
    order_type: OrderType
    time_in_force: TimeInForce = TimeInForce.DAY
    quantity: int = Field(gt=0)
    limit_price: float | None = Field(default=None, gt=0)
    stop_price: float | None = Field(default=None, gt=0)
    strategy_id: str | None = Field(default=None, max_length=128)


class OrderResponse(BaseModel):
    id: int
    client_order_id: str
    portfolio_id: int
    symbol: str
    side: OrderSide
    order_type: OrderType
    time_in_force: TimeInForce
    quantity: int
    filled_quantity: int
    limit_price: float | None
    stop_price: float | None
    average_fill_price: float
    status: OrderStatus
    broker_order_id: str | None
    strategy_id: str | None
    reject_reason: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
