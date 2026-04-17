"""Repository for loading and saving game sessions."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from sqlalchemy.orm import Session as DbSession

from structured_freedom.models.npc import NPC
from structured_freedom.models.player import Player
from structured_freedom.models.world_state import WorldState
from structured_freedom.persistence.orm.models import SessionRow, TurnRow


@dataclass
class GameSession:
    """In-memory representation of a full game session."""

    id: str
    player: Player
    world: WorldState
    npcs: dict[str, NPC]
    turn_number: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class GameRepository:
    """Loads and saves game sessions using a SQLAlchemy session."""

    def __init__(self, db: DbSession) -> None:
        self._db = db

    def create_session(
        self,
        player: Player,
        world: WorldState,
        npcs: dict[str, NPC],
    ) -> GameSession:
        session_id = str(uuid.uuid4())
        row = SessionRow(
            id=session_id,
            player_json=player.model_dump_json(),
            world_json=world.model_dump_json(),
            npcs_json=json.dumps({k: v.model_dump() for k, v in npcs.items()}),
            turn_number=0,
        )
        self._db.add(row)
        self._db.commit()
        return GameSession(
            id=session_id,
            player=player,
            world=world,
            npcs=npcs,
            turn_number=0,
        )

    def load_session(self, session_id: str) -> GameSession | None:
        row = self._db.get(SessionRow, session_id)
        if row is None:
            return None
        player = Player.model_validate_json(row.player_json)
        world = WorldState.model_validate_json(row.world_json)
        raw_npcs = json.loads(row.npcs_json)
        npcs = {k: NPC.model_validate(v) for k, v in raw_npcs.items()}
        return GameSession(
            id=row.id,
            player=player,
            world=world,
            npcs=npcs,
            turn_number=row.turn_number,
            created_at=row.created_at,
        )

    def save_session(self, session: GameSession) -> None:
        row = self._db.get(SessionRow, session.id)
        if row is None:
            raise ValueError(f"Session {session.id!r} not found.")
        row.player_json = session.player.model_dump_json()
        row.world_json = session.world.model_dump_json()
        row.npcs_json = json.dumps({k: v.model_dump() for k, v in session.npcs.items()})
        row.turn_number = session.turn_number
        self._db.commit()

    def append_turn(
        self,
        session_id: str,
        turn_number: int,
        raw_input: str,
        parsed_intent_json: str | None,
        validation_success: bool,
        state_changes_json: str | None,
        narration: str | None,
    ) -> None:
        row = TurnRow(
            session_id=session_id,
            turn_number=turn_number,
            raw_input=raw_input,
            parsed_intent_json=parsed_intent_json,
            validation_success=int(validation_success),
            state_changes_json=state_changes_json,
            narration=narration,
        )
        self._db.add(row)
        self._db.commit()

    def get_turns(self, session_id: str, limit: int = 20) -> list[TurnRow]:
        return (
            self._db.query(TurnRow)
            .filter(TurnRow.session_id == session_id)
            .order_by(TurnRow.turn_number.desc())
            .limit(limit)
            .all()
        )
