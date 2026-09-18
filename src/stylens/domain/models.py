"""Provider-independent consultation domain models."""

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SessionStatus(StrEnum):
    CREATED = "created"
    CONSENTED = "consented"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    CLOSED = "closed"
    DELETED = "deleted"


class ConsentRecord(BaseModel):
    notice_version: str = Field(min_length=1, max_length=32)
    accepted: bool
    adult_confirmed: bool
    accepted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ConsultationSession(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    status: SessionStatus = SessionStatus.CREATED
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    consent: ConsentRecord | None = None

    def record_consent(self, consent: ConsentRecord) -> None:
        if not consent.accepted or not consent.adult_confirmed:
            raise ValueError("Explicit adult consent is required before processing images.")
        self.consent = consent
        self.status = SessionStatus.CONSENTED

