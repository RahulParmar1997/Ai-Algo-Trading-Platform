from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.portfolio import PortfolioResponse, PortfolioValueResponse
from app.schemas.position import PositionResponse
from app.services.portfolio import (
    get_portfolio,
    get_portfolio_holdings,
    get_portfolio_value,
)

router = APIRouter(prefix="/api/portfolios", tags=["portfolio"])


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def read_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
) -> PortfolioResponse:
    portfolio = get_portfolio(db, portfolio_id)
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    return portfolio


@router.get("/{portfolio_id}/value", response_model=PortfolioValueResponse)
def read_portfolio_value(
    portfolio_id: int,
    db: Session = Depends(get_db),
) -> PortfolioValueResponse:
    value = get_portfolio_value(db, portfolio_id)
    if value is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    return value


@router.get("/{portfolio_id}/positions", response_model=list[PositionResponse])
def read_portfolio_positions(
    portfolio_id: int,
    db: Session = Depends(get_db),
) -> list[PositionResponse]:
    positions = get_portfolio_holdings(db, portfolio_id)
    if positions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    return positions
