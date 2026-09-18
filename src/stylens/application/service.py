"""Consultation workflow independent from HTTP and model providers."""

from hashlib import sha256
from io import BytesIO
from uuid import UUID

from PIL import Image, UnidentifiedImageError

from stylens.application.exceptions import (
    ConsentRequiredError,
    InvalidImageError,
    PrototypeDataPolicyError,
    SessionNotFoundError,
)
from stylens.domain.models import ConsentRecord, ConsultationSession, ImageAsset
from stylens.domain.ports import ArtifactStore, SessionRepository

ALLOWED_FORMATS = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}


class ConsultationService:
    def __init__(
        self,
        sessions: SessionRepository,
        artifacts: ArtifactStore,
        *,
        max_upload_bytes: int,
        synthetic_data_only: bool,
    ) -> None:
        self._sessions = sessions
        self._artifacts = artifacts
        self.max_upload_bytes = max_upload_bytes
        self._synthetic_data_only = synthetic_data_only

    async def create_session(self) -> ConsultationSession:
        session = ConsultationSession()
        await self._sessions.create(session)
        return session

    async def get_session(self, session_id: UUID) -> ConsultationSession:
        session = await self._sessions.get(str(session_id))
        if session is None:
            raise SessionNotFoundError(str(session_id))
        return session

    async def record_consent(
        self, session_id: UUID, consent: ConsentRecord
    ) -> ConsultationSession:
        session = await self.get_session(session_id)
        session.record_consent(consent)
        await self._sessions.save(session)
        return session

    async def upload_image(
        self,
        session_id: UUID,
        content: bytes,
        declared_media_type: str | None,
        *,
        synthetic_confirmed: bool,
    ) -> ConsultationSession:
        session = await self.get_session(session_id)
        if session.consent is None:
            raise ConsentRequiredError("Consent is required before image upload.")
        if self._synthetic_data_only and not synthetic_confirmed:
            raise PrototypeDataPolicyError(
                "The hackathon prototype accepts synthetic people only."
            )
        if not content or len(content) > self.max_upload_bytes:
            raise InvalidImageError("Image must be non-empty and within the configured size limit.")

        try:
            with Image.open(BytesIO(content)) as image:
                image.verify()
            with Image.open(BytesIO(content)) as image:
                image_format = image.format or ""
                detected_media_type = ALLOWED_FORMATS.get(image_format)
                width, height = image.size
                image.load()
                sanitized = image.copy()
        except (Image.DecompressionBombError, UnidentifiedImageError, OSError) as error:
            raise InvalidImageError("The upload is not a valid supported image.") from error

        if detected_media_type is None:
            raise InvalidImageError("Only JPEG, PNG, and WebP images are supported.")
        if declared_media_type and declared_media_type != detected_media_type:
            raise InvalidImageError("Declared and detected image types do not match.")
        if width < 1024 or height < 1024:
            raise InvalidImageError("Image dimensions must be at least 1024 x 1024 pixels.")

        sanitized_output = BytesIO()
        if image_format == "JPEG":
            sanitized = sanitized.convert("RGB")
            sanitized.save(sanitized_output, format="JPEG", quality=95, optimize=True)
        elif image_format == "PNG":
            sanitized.save(sanitized_output, format="PNG", optimize=True)
        else:
            sanitized.save(sanitized_output, format="WEBP", quality=95, method=4)
        sanitized_content = sanitized_output.getvalue()

        metadata = ImageAsset(
            media_type=detected_media_type,
            width=width,
            height=height,
            size_bytes=len(sanitized_content),
            sha256=sha256(sanitized_content).hexdigest(),
            source_classification="synthetic",
        )
        await self._artifacts.save_image(
            session_id=str(session_id), content=sanitized_content
        )
        session.record_validated_image(metadata)
        await self._sessions.save(session)
        return session

    async def delete_session(self, session_id: UUID) -> None:
        await self._artifacts.delete_session(session_id=str(session_id))
        deleted = await self._sessions.delete(str(session_id))
        if not deleted:
            raise SessionNotFoundError(str(session_id))
