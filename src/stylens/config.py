"""Validated application configuration."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="STYLENS_",
        extra="ignore",
    )

    app_name: str = "StyLens"
    environment: str = "development"
    api_prefix: str = "/api/v1"
    session_ttl_minutes: int = Field(default=60, ge=15, le=240)
    max_upload_mb: int = Field(default=15, ge=1, le=25)
    artifact_retention_minutes: int = Field(default=60, ge=15, le=1440)


@lru_cache
def get_settings() -> Settings:
    return Settings()

