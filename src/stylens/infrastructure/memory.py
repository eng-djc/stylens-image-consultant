"""Process-local adapters for the hackathon MVP.

Data is intentionally lost when the process stops. Production deployments must
replace these adapters with approved encrypted storage.
"""

from asyncio import Lock

from stylens.domain.models import ConsultationSession


class InMemorySessionRepository:
    def __init__(self) -> None:
        self._items: dict[str, ConsultationSession] = {}
        self._lock = Lock()

    async def create(self, session: ConsultationSession) -> None:
        async with self._lock:
            self._items[str(session.session_id)] = session.model_copy(deep=True)

    async def get(self, session_id: str) -> ConsultationSession | None:
        async with self._lock:
            session = self._items.get(session_id)
            return session.model_copy(deep=True) if session else None

    async def save(self, session: ConsultationSession) -> None:
        async with self._lock:
            self._items[str(session.session_id)] = session.model_copy(deep=True)

    async def delete(self, session_id: str) -> bool:
        async with self._lock:
            return self._items.pop(session_id, None) is not None


class InMemoryArtifactStore:
    def __init__(self) -> None:
        self._images: dict[str, bytearray] = {}
        self._lock = Lock()

    async def save_image(self, *, session_id: str, content: bytes) -> None:
        async with self._lock:
            previous = self._images.pop(session_id, None)
            if previous is not None:
                previous[:] = b"\x00" * len(previous)
            self._images[session_id] = bytearray(content)

    async def delete_session(self, *, session_id: str) -> None:
        async with self._lock:
            image = self._images.pop(session_id, None)
            if image is not None:
                image[:] = b"\x00" * len(image)

