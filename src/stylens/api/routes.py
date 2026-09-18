"""Initial public API routes."""

from fastapi import APIRouter, status
from pydantic import BaseModel

from stylens.domain.models import ConsultationSession, ConsentRecord

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="stylens")


@router.post("/sessions", response_model=ConsultationSession, status_code=status.HTTP_201_CREATED)
async def create_session() -> ConsultationSession:
    return ConsultationSession()


@router.post("/sessions/{session_id}/consent", response_model=ConsultationSession)
async def record_consent(session_id: str, consent: ConsentRecord) -> ConsultationSession:
    session = ConsultationSession(session_id=session_id)
    session.record_consent(consent)
    return session

