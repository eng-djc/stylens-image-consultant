"""Interfaces that keep domain logic independent from AI providers."""

from typing import Protocol

from stylens.domain.models import ConsultationSession


class SessionRepository(Protocol):
    async def create(self, session: ConsultationSession) -> None: ...

    async def get(self, session_id: str) -> ConsultationSession | None: ...

    async def save(self, session: ConsultationSession) -> None: ...

    async def delete(self, session_id: str) -> bool: ...


class AnalysisProvider(Protocol):
    async def analyze(self, *, session_id: str, image_reference: str) -> dict[str, object]: ...


class ImageEditingProvider(Protocol):
    async def edit(
        self,
        *,
        session_id: str,
        image_reference: str,
        authorized_mask_reference: str,
        instruction: str,
    ) -> str: ...


class ArtifactStore(Protocol):
    async def save_image(self, *, session_id: str, content: bytes) -> None: ...

    async def delete_session(self, *, session_id: str) -> None: ...
