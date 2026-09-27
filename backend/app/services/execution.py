from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.order import Order, OrderSide, OrderStatus, OrderType
from app.models.position import Position
from app.models.portfolio import Portfolio
from app.models.trade import Trade
from app.models.transaction import Transaction, TransactionSide


class ExecutionRejected(Exception):
    """Raised when an order cannot be executed by the selected execution venue."""


@dataclass(frozen=True)
class MarketQuote:
    symbol: str
    bid: float
    ask: float
    last: float

    @property
    def market_price(self) -> float:
        return self.ask if self.ask > 0 else self.last


def _get_or_create_position(db: Session, portfolio_id: int, symbol: str) -> Position:
    position = (
        db.query(Position)
        .filter(Position.portfolio_id == portfolio_id, Position.symbol == symbol)
        .one_or_none()
    )
    if position is None:
        position = Position(
            portfolio_id=portfolio_id,
            symbol=symbol,
            quantity=0,
            average_price=0.0,
            current_price=0.0,
        )
        db.add(position)
        db.flush()
    return position


def _apply_fill_to_position(
    position: Position,
    side: OrderSide,
    quantity: int,
    price: float,
) -> float:
    """Apply an average-cost signed position update and return realized P&L."""
    signed_fill = quantity if side == OrderSide.BUY else -quantity
    old_qty = position.quantity
    old_avg = position.average_price
    realized = 0.0

    if old_qty == 0:
        position.quantity = signed_fill
        position.average_price = price
    elif old_qty > 0 and signed_fill > 0:
        new_qty = old_qty + signed_fill
        position.average_price = ((old_qty * old_avg) + (signed_fill * price)) / new_qty
        position.quantity = new_qty
    elif old_qty < 0 and signed_fill < 0:
        old_abs = abs(old_qty)
        fill_abs = abs(signed_fill)
        new_abs = old_abs + fill_abs
        position.average_price = ((old_abs * old_avg) + (fill_abs * price)) / new_abs
        position.quantity = -new_abs
    elif old_qty > 0 and signed_fill < 0:
        close_qty = min(old_qty, abs(signed_fill))
        realized = (price - old_avg) * close_qty
        remaining = old_qty - close_qty
        excess = abs(signed_fill) - close_qty
        if remaining > 0:
            position.quantity = remaining
            position.average_price = old_avg
        elif excess > 0:
            position.quantity = -excess
            position.average_price = price
        else:
            position.quantity = 0
            position.average_price = 0.0
    else:
        close_qty = min(abs(old_qty), signed_fill)
        realized = (old_avg - price) * close_qty
        remaining = abs(old_qty) - close_qty
        excess = signed_fill - close_qty
        if remaining > 0:
            position.quantity = -remaining
            position.average_price = old_avg
        elif excess > 0:
            position.quantity = excess
            position.average_price = price
        else:
            position.quantity = 0
            position.average_price = 0.0

    position.current_price = price
    return realized


def _recalculate_portfolio(portfolio: Portfolio) -> None:
    market_value = sum(
        position.quantity * position.current_price for position in portfolio.positions
    )
    portfolio.equity = portfolio.cash_balance + market_value
    portfolio.buying_power = max(0.0, portfolio.cash_balance)


class PaperBroker:
    """Deterministic local broker used for paper trading and integration tests."""

    name = "paper"

    def submit_market_order(
        self,
        db: Session,
        order: Order,
        *,
        quote: MarketQuote,
        fee_rate: float = 0.0005,
        executed_at: datetime | None = None,
    ) -> Trade:
        if order.order_type != OrderType.MARKET:
            raise ExecutionRejected("The initial paper broker supports market orders only.")

        if quote.symbol != order.symbol or quote.market_price <= 0:
            raise ExecutionRejected("A valid quote for the order symbol is required.")

        if order.status not in {OrderStatus.NEW, OrderStatus.ACCEPTED}:
            raise ExecutionRejected(f"Order cannot be executed from status={order.status.value}.")

        portfolio = order.portfolio
        fill_price = quote.market_price
        notional = order.quantity * fill_price
        fees = notional * fee_rate

        if order.side == OrderSide.BUY and portfolio.cash_balance < notional + fees:
            raise ExecutionRejected("Insufficient cash for paper order.")

        position = _get_or_create_position(db, portfolio.id, order.symbol)
        realized_pnl = _apply_fill_to_position(
            position=position,
            side=order.side,
            quantity=order.quantity,
            price=fill_price,
        )

        cash_delta = -notional - fees if order.side == OrderSide.BUY else notional - fees
        portfolio.cash_balance += cash_delta

        execution_id = str(uuid4())
        trade = Trade(
            order_id=order.id,
            portfolio_id=portfolio.id,
            symbol=order.symbol,
            side=order.side.value,
            quantity=order.quantity,
            price=fill_price,
            fees=fees,
            executed_at=executed_at or datetime.utcnow(),
            execution_id=execution_id,
        )
        db.add(trade)

        transaction = Transaction(
            portfolio_id=portfolio.id,
            symbol=order.symbol,
            side=(
                TransactionSide.BUY
                if order.side == OrderSide.BUY
                else TransactionSide.SELL
            ),
            quantity=order.quantity,
            price=fill_price,
            fees=fees,
            realized_pnl=realized_pnl,
            cash_delta=cash_delta,
            reference=execution_id,
            occurred_at=executed_at or datetime.utcnow(),
        )
        db.add(transaction)

        order.status = OrderStatus.FILLED
        order.filled_quantity = order.quantity
        order.average_fill_price = fill_price
        order.broker_order_id = execution_id

        _recalculate_portfolio(portfolio)
        db.commit()
        db.refresh(trade)
        return trade
