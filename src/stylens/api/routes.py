"""HTTP adapter for the consultation workflow."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from pydantic import BaseModel

from stylens.application.exceptions import (
    ConsentRequiredError,
    InvalidImageError,
    SessionNotFoundError,
)
from stylens.application.service import ConsultationService
from stylens.dependencies import get_consultation_service
from stylens.domain.models import ConsentRecord, ConsultationSession

router = APIRouter()
Service = Annotated[ConsultationService, Depends(get_consultation_service)]


class HealthResponse(BaseModel):
    status: str
    service: str


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="stylens")


@router.post("/sessions", response_model=ConsultationSession, status_code=status.HTTP_201_CREATED)
async def create_session(service: Service) -> ConsultationSession:
    return await service.create_session()


@router.get("/sessions/{session_id}", response_model=ConsultationSession)
async def get_session(session_id: UUID, service: Service) -> ConsultationSession:
    try:
        return await service.get_session(session_id)
    except SessionNotFoundError as error:
        raise HTTPException(status_code=404, detail="Session not found.") from error


@router.post("/sessions/{session_id}/consent", response_model=ConsultationSession)
async def record_consent(
    session_id: UUID, consent: ConsentRecord, service: Service
) -> ConsultationSession:
    try:
        return await service.record_consent(session_id, consent)
    except SessionNotFoundError as error:
        raise HTTPException(status_code=404, detail="Session not found.") from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/sessions/{session_id}/image", response_model=ConsultationSession)
async def upload_image(
    session_id: UUID,
    service: Service,
    image: Annotated[UploadFile, File(description="Consenting adult consultation image")],
) -> ConsultationSession:
    try:
        content = await image.read(service.max_upload_bytes + 1)
        return await service.upload_image(session_id, content, image.content_type)
    except SessionNotFoundError as error:
        raise HTTPException(status_code=404, detail="Session not found.") from error
    except ConsentRequiredError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except InvalidImageError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    finally:
        await image.close()


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: UUID, service: Service) -> Response:
    try:
        await service.delete_session(session_id)
    except SessionNotFoundError as error:
        raise HTTPException(status_code=404, detail="Session not found.") from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
