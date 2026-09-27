from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.order import Order, OrderStatus
from app.models.trade import Trade


def get_order(db: Session, order_id: int) -> Order | None:
    return db.scalar(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.portfolio))
    )


def list_orders(
    db: Session,
    portfolio_id: int,
    limit: int = 100,
    offset: int = 0,
) -> list[Order]:
    return list(
        db.scalars(
            select(Order)
            .where(Order.portfolio_id == portfolio_id)
            .order_by(Order.created_at.desc(), Order.id.desc())
            .limit(limit)
            .offset(offset)
        )
    )


def get_order_trades(db: Session, order_id: int) -> list[Trade]:
    return list(
        db.scalars(
            select(Trade)
            .where(Trade.order_id == order_id)
            .order_by(Trade.executed_at.asc(), Trade.id.asc())
        )
    )


def create_order(db: Session, *, portfolio_id: int, **kwargs) -> Order:
    order = Order(portfolio_id=portfolio_id, status=OrderStatus.NEW, **kwargs)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def cancel_order(db: Session, order: Order) -> Order:
    if order.status in {
        OrderStatus.FILLED,
        OrderStatus.CANCELED,
        OrderStatus.REJECTED,
    }:
        return order

    order.status = OrderStatus.CANCELED
    db.commit()
    db.refresh(order)
    return order
