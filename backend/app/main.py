from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.portfolio import router as portfolio_router
from app.api.trading import router as trading_router
from app.core.config import get_settings
from app.core.database import Base, engine
from app.models import (  # noqa: F401
    Order,
    Portfolio,
    PortfolioSnapshot,
    Position,
    Trade,
    Transaction,
    User,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )
    application.include_router(health_router)
    application.include_router(auth_router)
    application.include_router(portfolio_router)
    application.include_router(trading_router)
    return application


app = create_app()
