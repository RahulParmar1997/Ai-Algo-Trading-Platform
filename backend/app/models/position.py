from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_price: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    current_price: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id"), index=True, nullable=False
    )

    portfolio: Mapped["Portfolio"] = relationship(back_populates="positions")
