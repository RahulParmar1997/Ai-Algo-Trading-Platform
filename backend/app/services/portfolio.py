from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.models.user import User


def get_user_portfolio(db: Session, user: User) -> Portfolio | None:
    return db.scalar(
        select(Portfolio)
        .where(Portfolio.user_id == user.id)
        .order_by(Portfolio.id.asc())
    )


def get_portfolio_value(db: Session, user: User) -> dict[str, float]:
    portfolio = get_user_portfolio(db, user)
    if portfolio is None:
        return {"cash_balance": 0.0, "equity": 0.0, "buying_power": 0.0}

    return {
        "cash_balance": portfolio.cash_balance,
        "equity": portfolio.equity,
        "buying_power": portfolio.buying_power,
    }
