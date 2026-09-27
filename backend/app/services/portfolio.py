from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.portfolio import Portfolio
from app.models.position import Position
from app.models.user import User


def get_user_portfolio(db: Session, user: User) -> Portfolio | None:
    return db.scalar(
        select(Portfolio)
        .where(Portfolio.user_id == user.id)
        .options(selectinload(Portfolio.positions))
        .order_by(Portfolio.id.asc())
    )


def get_portfolio(db: Session, portfolio_id: int) -> Portfolio | None:
    return db.scalar(
        select(Portfolio)
        .where(Portfolio.id == portfolio_id)
        .options(selectinload(Portfolio.positions))
    )


def get_portfolio_value(db: Session, portfolio_id: int) -> dict[str, float] | None:
    portfolio = get_portfolio(db, portfolio_id)
    if portfolio is None:
        return None

    return {
        "cash_balance": portfolio.cash_balance,
        "equity": portfolio.equity,
        "buying_power": portfolio.buying_power,
    }


def get_portfolio_holdings(db: Session, portfolio_id: int) -> list[Position] | None:
    portfolio = get_portfolio(db, portfolio_id)
    if portfolio is None:
        return None
    return portfolio.positions
