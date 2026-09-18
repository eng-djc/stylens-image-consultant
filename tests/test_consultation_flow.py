from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from stylens.dependencies import get_consultation_service
from stylens.infrastructure.memory import InMemoryArtifactStore
from stylens.main import app


def _valid_image() -> bytes:
    output = BytesIO()
    Image.new("RGB", (1024, 1024), color=(60, 80, 100)).save(output, format="PNG")
    return output.getvalue()


def _jpeg_with_exif() -> bytes:
    output = BytesIO()
    image = Image.new("RGB", (1024, 1024), color=(60, 80, 100))
    exif = Image.Exif()
    exif[0x010F] = "Synthetic camera location metadata"
    image.save(output, format="JPEG", exif=exif)
    return output.getvalue()


def test_consultation_flow_requires_consent_and_deletes_session() -> None:
    get_consultation_service.cache_clear()
    with TestClient(app) as client:
        created = client.post("/api/v1/sessions")
        session_id = created.json()["session_id"]

        denied = client.post(
            f"/api/v1/sessions/{session_id}/image",
            data={"synthetic_confirmed": "true"},
            files={"image": ("client.png", _valid_image(), "image/png")},
        )
        assert denied.status_code == 403

        consented = client.post(
            f"/api/v1/sessions/{session_id}/consent",
            json={"notice_version": "1.0", "accepted": True, "adult_confirmed": True},
        )
        assert consented.status_code == 200
        assert consented.json()["status"] == "consented"

        uploaded = client.post(
            f"/api/v1/sessions/{session_id}/image",
            data={"synthetic_confirmed": "true"},
            files={"image": ("client.png", _valid_image(), "image/png")},
        )
        assert uploaded.status_code == 200
        assert uploaded.json()["status"] == "image_validated"
        assert uploaded.json()["image"]["width"] == 1024

        deleted = client.delete(f"/api/v1/sessions/{session_id}")
        assert deleted.status_code == 204
        assert client.get(f"/api/v1/sessions/{session_id}").status_code == 404


def test_rejects_invalid_image_content() -> None:
    get_consultation_service.cache_clear()
    with TestClient(app) as client:
        session_id = client.post("/api/v1/sessions").json()["session_id"]
        client.post(
            f"/api/v1/sessions/{session_id}/consent",
            json={"notice_version": "1.0", "accepted": True, "adult_confirmed": True},
        )

        response = client.post(
            f"/api/v1/sessions/{session_id}/image",
            data={"synthetic_confirmed": "true"},
            files={"image": ("fake.png", b"not-an-image", "image/png")},
        )

        assert response.status_code == 422


def test_rejects_real_person_image_attestation() -> None:
    get_consultation_service.cache_clear()
    with TestClient(app) as client:
        session_id = client.post("/api/v1/sessions").json()["session_id"]
        client.post(
            f"/api/v1/sessions/{session_id}/consent",
            json={"notice_version": "1.0", "accepted": True, "adult_confirmed": True},
        )

        response = client.post(
            f"/api/v1/sessions/{session_id}/image",
            data={"synthetic_confirmed": "false"},
            files={"image": ("client.png", _valid_image(), "image/png")},
        )

        assert response.status_code == 403
        assert "synthetic people only" in response.json()["detail"]


def test_ephemeral_store_overwrites_and_zeroes_previous_image() -> None:
    store = InMemoryArtifactStore()
    previous = bytearray(b"sensitive-image")
    store._images["session"] = previous

    import asyncio

    asyncio.run(store.save_image(session_id="session", content=b"replacement"))

    assert previous == bytearray(len(previous))


def test_upload_reencoding_removes_exif_metadata() -> None:
    get_consultation_service.cache_clear()
    with TestClient(app) as client:
        session_id = client.post("/api/v1/sessions").json()["session_id"]
        client.post(
            f"/api/v1/sessions/{session_id}/consent",
            json={"notice_version": "1.0", "accepted": True, "adult_confirmed": True},
        )
        response = client.post(
            f"/api/v1/sessions/{session_id}/image",
            data={"synthetic_confirmed": "true"},
            files={"image": ("synthetic.jpg", _jpeg_with_exif(), "image/jpeg")},
        )
        assert response.status_code == 200
        assert response.json()["image"]["source_classification"] == "synthetic"

        service = get_consultation_service()
        stored = bytes(service._artifacts._images[session_id])
        with Image.open(BytesIO(stored)) as sanitized:
            assert len(sanitized.getexif()) == 0
