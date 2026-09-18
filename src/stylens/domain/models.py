"""Provider-independent consultation domain models."""

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SessionStatus(StrEnum):
    CREATED = "created"
    CONSENTED = "consented"
    IMAGE_VALIDATED = "image_validated"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    CLOSED = "closed"
    DELETED = "deleted"


class ConsentRecord(BaseModel):
    notice_version: str = Field(min_length=1, max_length=32)
    accepted: bool
    adult_confirmed: bool
    accepted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ImageAsset(BaseModel):
    """Non-sensitive metadata for a sanitized, ephemeral image."""

    media_type: str
    width: int = Field(ge=1024)
    height: int = Field(ge=1024)
    size_bytes: int = Field(gt=0)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class ConsultationSession(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    status: SessionStatus = SessionStatus.CREATED
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    consent: ConsentRecord | None = None
    image: ImageAsset | None = None

    def record_consent(self, consent: ConsentRecord) -> None:
        if not consent.accepted or not consent.adult_confirmed:
            raise ValueError("Explicit adult consent is required before processing images.")
        self.consent = consent
        self.status = SessionStatus.CONSENTED

    def record_validated_image(self, image: ImageAsset) -> None:
        if self.status is not SessionStatus.CONSENTED:
            raise ValueError("Valid consent is required before accepting an image.")
        self.image = image
        self.status = SessionStatus.IMAGE_VALIDATED
