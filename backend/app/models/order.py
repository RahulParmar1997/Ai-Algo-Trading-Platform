from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class TimeInForce(str, Enum):
    DAY = "day"
    GTC = "gtc"
    IOC = "ioc"
    FOK = "fok"


class OrderStatus(str, Enum):
    NEW = "new"
    ACCEPTED = "accepted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_order_id: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, default=lambda: str(uuid4())
    )
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    side: Mapped[OrderSide] = mapped_column(String(10), nullable=False)
    order_type: Mapped[OrderType] = mapped_column(String(20), nullable=False)
    time_in_force: Mapped[TimeInForce] = mapped_column(String(10), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    filled_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    limit_price: Mapped[float | None] = mapped_column(Float)
    stop_price: Mapped[float | None] = mapped_column(Float)
    average_fill_price: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(String(24), default=OrderStatus.NEW, nullable=False)
    broker_order_id: Mapped[str | None] = mapped_column(String(128), index=True)
    strategy_id: Mapped[str | None] = mapped_column(String(128), index=True)
    reject_reason: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    portfolio: Mapped["Portfolio"] = relationship(back_populates="orders")
