from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Algo Trading Platform"
    environment: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./trading.db"
    api_prefix: str = "/api"
    cors_origins: str = "*"
    secret_key: str = "CHANGE-ME-IN-PRODUCTION"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
