from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.performance import PortfolioSnapshot
from app.models.portfolio import Portfolio
from app.models.position import Position
from app.models.transaction import Transaction
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


def get_portfolio_analytics(db: Session, portfolio_id: int) -> dict | None:
    portfolio = get_portfolio(db, portfolio_id)
    if portfolio is None:
        return None

    realized_pnl = float(
        db.scalar(
            select(func.coalesce(func.sum(Transaction.realized_pnl), 0.0))
            .where(Transaction.portfolio_id == portfolio_id)
        )
        or 0.0
    )
    total_fees = float(
        db.scalar(
            select(func.coalesce(func.sum(Transaction.fees), 0.0))
            .where(Transaction.portfolio_id == portfolio_id)
        )
        or 0.0
    )

    allocation = []
    market_value = 0.0
    unrealized_pnl = 0.0

    for position in portfolio.positions:
        position_value = position.quantity * position.current_price
        position_pnl = (position.current_price - position.average_price) * position.quantity
        market_value += position_value
        unrealized_pnl += position_pnl
        allocation.append(
            {
                "symbol": position.symbol,
                "quantity": position.quantity,
                "market_value": position_value,
                "allocation_pct": (position_value / portfolio.equity * 100.0)
                if portfolio.equity
                else 0.0,
                "unrealized_pnl": position_pnl,
            }
        )

    net_pnl = realized_pnl + unrealized_pnl - total_fees
    baseline_equity = 100000.0
    first_snapshot = db.scalar(
        select(PortfolioSnapshot)
        .where(PortfolioSnapshot.portfolio_id == portfolio_id)
        .order_by(PortfolioSnapshot.captured_at.asc(), PortfolioSnapshot.id.asc())
        .limit(1)
    )
    if first_snapshot and first_snapshot.equity:
        baseline_equity = first_snapshot.equity
    return_pct = (net_pnl / baseline_equity * 100.0) if baseline_equity else 0.0

    return {
        "portfolio_id": portfolio.id,
        "cash_balance": portfolio.cash_balance,
        "equity": portfolio.equity,
        "buying_power": portfolio.buying_power,
        "market_value": market_value,
        "realized_pnl": realized_pnl,
        "unrealized_pnl": unrealized_pnl,
        "total_fees": total_fees,
        "net_pnl": net_pnl,
        "return_pct": return_pct,
        "invested_pct": (market_value / portfolio.equity * 100.0) if portfolio.equity else 0.0,
        "allocation": allocation,
    }


def get_transactions(
    db: Session,
    portfolio_id: int,
    limit: int = 100,
    offset: int = 0,
) -> list[Transaction]:
    return list(
        db.scalars(
            select(Transaction)
            .where(Transaction.portfolio_id == portfolio_id)
            .order_by(Transaction.occurred_at.desc(), Transaction.id.desc())
            .limit(limit)
            .offset(offset)
        )
    )


def get_performance_snapshots(
    db: Session,
    portfolio_id: int,
    limit: int = 365,
    offset: int = 0,
) -> list[PortfolioSnapshot]:
    return list(
        db.scalars(
            select(PortfolioSnapshot)
            .where(PortfolioSnapshot.portfolio_id == portfolio_id)
            .order_by(PortfolioSnapshot.captured_at.desc(), PortfolioSnapshot.id.desc())
            .limit(limit)
            .offset(offset)
        )
    )


def record_portfolio_snapshot(
    db: Session,
    portfolio_id: int,
    *,
    captured_at=None,
) -> PortfolioSnapshot | None:
    portfolio = get_portfolio(db, portfolio_id)
    if portfolio is None:
        return None

    market_value = sum(
        position.quantity * position.current_price for position in portfolio.positions
    )
    equity = portfolio.cash_balance + market_value

    previous = db.scalar(
        select(PortfolioSnapshot)
        .where(PortfolioSnapshot.portfolio_id == portfolio_id)
        .order_by(PortfolioSnapshot.captured_at.desc(), PortfolioSnapshot.id.desc())
        .limit(1)
    )

    daily_return = ((equity / previous.equity) - 1.0) if previous and previous.equity else 0.0
    baseline_equity = 100000.0
    if previous and previous.cumulative_return != 0.0:
        baseline_equity = previous.equity / (1.0 + previous.cumulative_return)
    cumulative_return = ((equity / baseline_equity) - 1.0) if baseline_equity else 0.0
    prior_peak = max(
        [s.equity for s in get_performance_snapshots(db, portfolio_id, limit=10000)]
        + [100000.0]
    )
    drawdown = ((equity / prior_peak) - 1.0) if prior_peak else 0.0

    snapshot = PortfolioSnapshot(
        portfolio_id=portfolio_id,
        captured_at=captured_at or datetime.utcnow(),
        cash_balance=portfolio.cash_balance,
        market_value=market_value,
        equity=equity,
        daily_return=daily_return,
        cumulative_return=cumulative_return,
        drawdown=drawdown,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot
