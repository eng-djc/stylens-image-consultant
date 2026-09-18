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
    max_image_pixels: int = Field(default=16_777_216, ge=1_048_576, le=25_000_000)


@lru_cache
def get_settings() -> Settings:
    return Settings()
