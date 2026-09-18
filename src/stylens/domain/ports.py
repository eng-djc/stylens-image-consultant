"""Interfaces that keep domain logic independent from AI providers."""

from typing import Protocol


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
    async def delete_session(self, *, session_id: str) -> None: ...

