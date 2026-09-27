from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.portfolio import PortfolioResponse, PortfolioValueResponse
from app.schemas.position import PositionResponse
from app.services.portfolio import (
    get_portfolio,
    get_portfolio_holdings,
    get_portfolio_value,
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
