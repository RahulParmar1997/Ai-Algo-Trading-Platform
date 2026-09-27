from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.order import Order, OrderStatus
from app.models.trade import Trade
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.schemas.trade import TradeResponse
from app.services.execution import ExecutionRejected, MarketQuote, PaperBroker
from app.services.orders import cancel_order, create_order, get_order, list_orders

router = APIRouter(prefix="/api/trading", tags=["trading"])


class PaperExecutionRequest(BaseModel):
    bid: float = Field(gt=0)
    ask: float = Field(gt=0)
    last: float = Field(gt=0)
    fee_rate: float = Field(default=0.0005, ge=0, le=0.1)


def owned_order_or_404(order: Order | None, current_user: User) -> Order:
    if order is None or order.portfolio.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def owned_portfolio_order_count(
    db: Session,
    portfolio_id: int,
    current_user: User,
) -> None:
    exists = db.scalar(
        select(Order.id)
        .where(
            Order.portfolio_id == portfolio_id,
            Order.portfolio.has(user_id=current_user.id),
        )
        .limit(1)
    )
    if exists is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")


@router.post("/orders/{portfolio_id}", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def submit_order(
    portfolio_id: int,
    request: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderResponse:
    owned_portfolio_order_count(db, portfolio_id, current_user)
    order = create_order(
        db,
        portfolio_id=portfolio_id,
        symbol=request.symbol.upper(),
        side=request.side,
        order_type=request.order_type,
        time_in_force=request.time_in_force,
        quantity=request.quantity,
        limit_price=request.limit_price,
        stop_price=request.stop_price,
        strategy_id=request.strategy_id,
    )
    return order


@router.get("/orders/{portfolio_id}", response_model=list[OrderResponse])
def read_orders(
    portfolio_id: int,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[OrderResponse]:
    owned_portfolio_order_count(db, portfolio_id, current_user)
    return list_orders(db, portfolio_id, limit=limit, offset=offset)


@router.get("/orders/detail/{order_id}", response_model=OrderResponse)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderResponse:
    order = get_order(db, order_id)
    return owned_order_or_404(order, current_user)


@router.post("/orders/detail/{order_id}/cancel", response_model=OrderResponse)
def cancel_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderResponse:
    order = owned_order_or_404(get_order(db, order_id), current_user)
    return cancel_order(db, order)


@router.post(
    "/orders/detail/{order_id}/paper-execute",
    response_model=TradeResponse,
)
def paper_execute(
    order_id: int,
    request: PaperExecutionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TradeResponse:
    order = get_order(db, order_id)
    order = owned_order_or_404(order, current_user)

    if order.status in {OrderStatus.FILLED, OrderStatus.CANCELED, OrderStatus.REJECTED}:
        raise HTTPException(status_code=409, detail="Order is not executable")

    try:
        trade = PaperBroker().submit_market_order(
            db,
            order,
            quote=MarketQuote(
                symbol=order.symbol,
                bid=request.bid,
                ask=request.ask,
                last=request.last,
            ),
            fee_rate=request.fee_rate,
        )
    except ExecutionRejected as exc:
        order.status = OrderStatus.REJECTED
        order.reject_reason = str(exc)
        db.commit()
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return trade
