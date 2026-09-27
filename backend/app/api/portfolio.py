from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.portfolio import PortfolioResponse, PortfolioValueResponse
from app.schemas.performance import PortfolioAnalyticsResponse, PortfolioSnapshotResponse
from app.schemas.position import PositionResponse
from app.schemas.transaction import TransactionResponse
from app.services.portfolio import (
    get_portfolio,
    get_portfolio_holdings,
    get_performance_snapshots,
    get_portfolio_analytics,
    get_portfolio_value,
    get_transactions,
)

router = APIRouter(prefix="/api/portfolios", tags=["portfolio"])


def owned_portfolio_or_404(
    portfolio_id: int,
    current_user: User,
    db: Session,
):
    portfolio = get_portfolio(db, portfolio_id)
    if portfolio is None or portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    return portfolio


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def read_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortfolioResponse:
    return owned_portfolio_or_404(portfolio_id, current_user, db)


@router.get("/{portfolio_id}/value", response_model=PortfolioValueResponse)
def read_portfolio_value(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortfolioValueResponse:
    owned_portfolio_or_404(portfolio_id, current_user, db)
    value = get_portfolio_value(db, portfolio_id)
    if value is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return value


@router.get("/{portfolio_id}/positions", response_model=list[PositionResponse])
def read_portfolio_positions(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PositionResponse]:
    owned_portfolio_or_404(portfolio_id, current_user, db)
    positions = get_portfolio_holdings(db, portfolio_id)
    if positions is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return positions



@router.get("/{portfolio_id}/analytics", response_model=PortfolioAnalyticsResponse)
def read_portfolio_analytics(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortfolioAnalyticsResponse:
    owned_portfolio_or_404(portfolio_id, current_user, db)
    analytics = get_portfolio_analytics(db, portfolio_id)
    if analytics is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return analytics


@router.get("/{portfolio_id}/transactions", response_model=list[TransactionResponse])
def read_portfolio_transactions(
    portfolio_id: int,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TransactionResponse]:
    owned_portfolio_or_404(portfolio_id, current_user, db)
    return get_transactions(db, portfolio_id, limit=limit, offset=offset)


@router.get("/{portfolio_id}/performance", response_model=list[PortfolioSnapshotResponse])
def read_portfolio_performance(
    portfolio_id: int,
    limit: int = Query(default=365, ge=1, le=2000),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PortfolioSnapshotResponse]:
    owned_portfolio_or_404(portfolio_id, current_user, db)
    return get_performance_snapshots(db, portfolio_id, limit=limit, offset=offset)
