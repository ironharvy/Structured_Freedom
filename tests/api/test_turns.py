"""Integration tests for the FastAPI turn and session endpoints."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from structured_freedom.app.api.app import create_app
from structured_freedom.app.api.routes import get_db
from structured_freedom.persistence.orm.models import Base


@pytest.fixture(scope="module")
def client():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        future=True,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def override_db():
        db = factory()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_db

    with TestClient(app) as c:
        yield c


def _mock_intent(action_type: str = "examine", target: str = "location"):
    intent = MagicMock()
    intent.action_type = action_type
    intent.target = target
    intent.is_plausible = True
    intent.rejection_reason = ""
    intent.model_dump_json.return_value = "{}"
    return intent


class TestSessionEndpoints:
    def test_create_session(self, client):
        res = client.post("/api/sessions", json={"player_name": "Hero"})
        assert res.status_code == 201
        data = res.json()
        assert "session_id" in data
        assert data["state"]["location_id"] == "village"

    def test_get_session(self, client):
        create_res = client.post("/api/sessions", json={"player_name": "Tester"})
        sid = create_res.json()["session_id"]

        res = client.get(f"/api/sessions/{sid}")
        assert res.status_code == 200
        assert res.json()["session_id"] == sid

    def test_get_nonexistent_session_returns_404(self, client):
        res = client.get("/api/sessions/00000000-0000-0000-0000-000000000000")
        assert res.status_code == 404


class TestTurnEndpoint:
    def _create_session(self, client):
        res = client.post("/api/sessions", json={"player_name": "Adventurer"})
        return res.json()["session_id"]

    def test_valid_action_returns_200(self, client):
        sid = self._create_session(client)
        narration = "You look around the village square."
        with (
            patch("structured_freedom.app.turns.IntentInterpreter") as mock_interp,
            patch("structured_freedom.app.turns.Narrator") as mock_narr,
        ):
            mock_interp.return_value.forward.return_value = _mock_intent()
            mock_narr.return_value.forward.return_value = narration

            res = client.post(
                f"/api/sessions/{sid}/turns", json={"action": "look around"}
            )
        assert res.status_code == 200
        data = res.json()
        assert "narration" in data
        assert "state" in data

    def test_empty_action_returns_422(self, client):
        sid = self._create_session(client)
        res = client.post(f"/api/sessions/{sid}/turns", json={"action": "   "})
        assert res.status_code == 422

    def test_nonexistent_session_turn_returns_404(self, client):
        res = client.post(
            "/api/sessions/00000000-0000-0000-0000-000000000000/turns",
            json={"action": "go north"},
        )
        assert res.status_code == 404

    def test_turn_increments_turn_number(self, client):
        sid = self._create_session(client)
        before = client.get(f"/api/sessions/{sid}").json()["state"]["turn_number"]

        with (
            patch("structured_freedom.app.turns.IntentInterpreter") as mock_interp,
            patch("structured_freedom.app.turns.Narrator") as mock_narr,
        ):
            mock_interp.return_value.forward.return_value = _mock_intent()
            mock_narr.return_value.forward.return_value = "You look around."
            client.post(f"/api/sessions/{sid}/turns", json={"action": "look around"})

        after = client.get(f"/api/sessions/{sid}").json()["state"]["turn_number"]
        assert after == before + 1
