from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.database import Base, engine
from app.models import Portfolio, Position, User  # noqa: F401

settings = get_settings()


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name, debug=settings.debug)

    @application.on_event("startup")
    def startup() -> None:
        Base.metadata.create_all(bind=engine)

    application.include_router(health_router)
    return application


app = create_app()
