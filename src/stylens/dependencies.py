"""Application dependency composition."""

from functools import lru_cache

from stylens.application.service import ConsultationService
from stylens.config import get_settings
from stylens.infrastructure.memory import InMemoryArtifactStore, InMemorySessionRepository


@lru_cache
def get_consultation_service() -> ConsultationService:
    settings = get_settings()
    return ConsultationService(
        InMemorySessionRepository(),
        InMemoryArtifactStore(),
        max_upload_bytes=settings.max_upload_mb * 1024 * 1024,
        max_image_pixels=settings.max_image_pixels,
    )
