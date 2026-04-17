"""FastAPI routers for session management and turn execution."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DbSession

from structured_freedom.app.api.schemas import (
    CreateSessionRequest,
    SessionResponse,
    StateSnapshot,
    TurnRequest,
    TurnResponse,
)
from structured_freedom.app.turns import run_turn_full
from structured_freedom.persistence.repositories.game_repo import GameRepository
from structured_freedom.world.fixtures import build_npcs, build_world
from structured_freedom.world.scenario import build_player

router = APIRouter(prefix="/api")


def _snapshot_from_session(session, world_data=None) -> StateSnapshot:
    player = session.player
    location = session.world.locations.get(player.current_location)
    return StateSnapshot(
        location_id=player.current_location,
        location_name=location.name if location else "",
        location_description=location.description if location else "",
        inventory=list(player.inventory),
        quests={
            qid: {
                "active": qs.active_objectives,
                "completed": qs.completed_objectives,
                "done": qs.is_completed,
            }
            for qid, qs in player.quests.items()
        },
        turn_number=session.turn_number,
    )


def get_db() -> DbSession:
    """FastAPI dependency — overridden in tests and at app startup."""
    raise RuntimeError("Database dependency not configured. Call configure_db() at startup.")


_db_factory = None


def configure_db(session_factory) -> None:
    """Set the database session factory used by the dependency."""
    global _db_factory, get_db

    def _get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    get_db.__code__ = _get_db.__code__
    router.dependency_overrides = {}


@router.post("/sessions", response_model=SessionResponse, status_code=201)
def create_session(
    body: CreateSessionRequest,
    db: DbSession = Depends(get_db),
) -> SessionResponse:
    repo = GameRepository(db)
    player = build_player(name=body.player_name)
    world = build_world()
    npcs = build_npcs()
    session = repo.create_session(player=player, world=world, npcs=npcs)
    return SessionResponse(
        session_id=session.id,
        state=_snapshot_from_session(session),
    )


@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: str,
    db: DbSession = Depends(get_db),
) -> SessionResponse:
    repo = GameRepository(db)
    session = repo.load_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")
    return SessionResponse(
        session_id=session.id,
        state=_snapshot_from_session(session),
    )


@router.post("/sessions/{session_id}/turns", response_model=TurnResponse)
def execute_turn(
    session_id: str,
    body: TurnRequest,
    db: DbSession = Depends(get_db),
) -> TurnResponse:
    if not body.action.strip():
        raise HTTPException(status_code=422, detail="Action must not be empty.")
    repo = GameRepository(db)
    session = repo.load_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    result = run_turn_full(
        action_text=body.action,
        session=session,
        repo=repo,
        use_ai=True,
    )

    snapshot = result["state_snapshot"]
    return TurnResponse(
        success=result["success"],
        narration=result["narration"],
        state=StateSnapshot(
            location_id=snapshot["location_id"],
            location_name=snapshot["location_name"],
            location_description=snapshot["location_description"],
            inventory=snapshot["inventory"],
            quests=snapshot["quests"],
            turn_number=snapshot["turn_number"],
        ),
    )
