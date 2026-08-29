"""
tests/test_visual_chat.py — Contract tests for POST /api/v1/chat/visual

Uses an in-memory SQLite database and mocks the PaliGemma service so
no real GPU or network call is needed during CI.
"""

from __future__ import annotations

import io
import os
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from PIL import Image as PILImage

# Force SQLite for tests
os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["PALIGEMMA_BACKEND_URL"] = "https://mock-colab.ngrok-free.dev"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_image_bytes(color: tuple = (73, 109, 137), size: tuple = (224, 224)) -> bytes:
    """Create a minimal in-memory JPEG for upload."""
    img = PILImage.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


MOCK_RESPONSE = {
    "question": "What quote is written on the tote bag?",
    "answer": "wash today shine tomorrow",
    "model": "PaliGemma 2 (LoRA fine-tuned)",
    "backend": "colab_proxy",
}


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def client():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    # Build an in-process SQLite engine for tests
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    from app.models.memory import Base
    Base.metadata.create_all(test_engine)

    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # Import app AFTER env vars are set
    from app.main import app
    from app.db.session import get_db

    def override_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestVisualChatEndpoint:
    """Tests for POST /api/v1/chat/visual"""

    def test_endpoint_returns_200_with_valid_image(self, client):
        """Happy path: valid JPEG + question → 200 with correct schema."""
        with patch(
            "app.services.paligemma_service.ask_visual",
            new=AsyncMock(return_value=MOCK_RESPONSE),
        ):
            resp = client.post(
                "/api/v1/chat/visual",
                files={"file": ("bag.jpg", _make_image_bytes(), "image/jpeg")},
                data={"question": "What quote is written on the tote bag?"},
            )

        assert resp.status_code == 200
        body = resp.json()
        assert body["question"] == "What quote is written on the tote bag?"
        assert body["answer"] == "wash today shine tomorrow"
        assert body["model"] == "PaliGemma 2 (LoRA fine-tuned)"
        assert body["backend"] == "colab_proxy"

    def test_required_fields_present(self, client):
        """Response must include question, answer, model, backend."""
        with patch(
            "app.services.paligemma_service.ask_visual",
            new=AsyncMock(return_value=MOCK_RESPONSE),
        ):
            resp = client.post(
                "/api/v1/chat/visual",
                files={"file": ("photo.jpg", _make_image_bytes(), "image/jpeg")},
                data={"question": "Where are my keys?"},
            )

        assert resp.status_code == 200
        body = resp.json()
        for field in ("question", "answer", "model", "backend"):
            assert field in body, f"Missing field: {field}"

    def test_unsupported_mime_type_returns_415(self, client):
        """Uploading a GIF should return HTTP 415."""
        resp = client.post(
            "/api/v1/chat/visual",
            files={"file": ("anim.gif", b"GIF89a\x01\x00\x01\x00", "image/gif")},
            data={"question": "What is this?"},
        )
        assert resp.status_code == 415

    def test_empty_question_returns_422(self, client):
        """Empty question string should fail validation (422)."""
        resp = client.post(
            "/api/v1/chat/visual",
            files={"file": ("img.jpg", _make_image_bytes(), "image/jpeg")},
            data={"question": ""},
        )
        assert resp.status_code == 422

    def test_missing_file_returns_422(self, client):
        """Missing file should return 422."""
        resp = client.post(
            "/api/v1/chat/visual",
            data={"question": "Where are my keys?"},
        )
        assert resp.status_code == 422

    def test_png_image_accepted(self, client):
        """PNG format should be accepted."""
        img = PILImage.new("RGB", (64, 64), color=(200, 100, 50))
        buf = io.BytesIO()
        img.save(buf, format="PNG")

        with patch(
            "app.services.paligemma_service.ask_visual",
            new=AsyncMock(return_value={**MOCK_RESPONSE, "answer": "on the table"}),
        ):
            resp = client.post(
                "/api/v1/chat/visual",
                files={"file": ("img.png", buf.getvalue(), "image/png")},
                data={"question": "What is on the table?"},
            )
        assert resp.status_code == 200

    def test_unavailable_backend_still_returns_200(self, client):
        """When Colab is down, the service returns an error message but still 200."""
        with patch(
            "app.services.paligemma_service.ask_visual",
            new=AsyncMock(return_value={
                "question": "test",
                "answer": "Could not reach the Colab backend.",
                "model": "none",
                "backend": "unavailable",
            }),
        ):
            resp = client.post(
                "/api/v1/chat/visual",
                files={"file": ("img.jpg", _make_image_bytes(), "image/jpeg")},
                data={"question": "test"},
            )
        assert resp.status_code == 200
        assert resp.json()["backend"] == "unavailable"
