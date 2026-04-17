"""Repository tests using SQLite in-memory database."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from structured_freedom.persistence.orm.models import Base
from structured_freedom.persistence.repositories.game_repo import GameRepository
from structured_freedom.world.fixtures import build_npcs, build_world
from structured_freedom.world.scenario import build_player


@pytest.fixture()
def db():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        future=True,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session = factory()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture()
def repo(db):
    return GameRepository(db)


class TestGameRepository:
    def test_create_and_load_session(self, repo):
        player = build_player("Test Hero")
        world = build_world()
        npcs = build_npcs()

        session = repo.create_session(player=player, world=world, npcs=npcs)
        assert session.id is not None
        assert session.turn_number == 0

        loaded = repo.load_session(session.id)
        assert loaded is not None
        assert loaded.player.name == "Test Hero"
        assert loaded.turn_number == 0

    def test_load_nonexistent_session_returns_none(self, repo):
        result = repo.load_session("00000000-0000-0000-0000-000000000000")
        assert result is None

    def test_save_session_persists_changes(self, repo):
        player = build_player()
        world = build_world()
        npcs = build_npcs()

        session = repo.create_session(player=player, world=world, npcs=npcs)
        session.player.move_to("tavern")
        session.turn_number = 3
        repo.save_session(session)

        loaded = repo.load_session(session.id)
        assert loaded.player.current_location == "tavern"
        assert loaded.turn_number == 3

    def test_append_turn_records_entry(self, repo):
        player = build_player()
        world = build_world()
        npcs = build_npcs()
        session = repo.create_session(player=player, world=world, npcs=npcs)

        repo.append_turn(
            session_id=session.id,
            turn_number=1,
            raw_input="go north",
            parsed_intent_json=None,
            validation_success=True,
            state_changes_json=None,
            narration="You walk north.",
        )

        turns = repo.get_turns(session.id)
        assert len(turns) == 1
        assert turns[0].raw_input == "go north"

    def test_world_flags_survive_roundtrip(self, repo):
        player = build_player()
        world = build_world()
        npcs = build_npcs()

        assert world.get_flag("gate_north_blocked") is True

        session = repo.create_session(player=player, world=world, npcs=npcs)
        loaded = repo.load_session(session.id)
        assert loaded.world.get_flag("gate_north_blocked") is True

    def test_npc_state_survives_roundtrip(self, repo):
        player = build_player()
        world = build_world()
        npcs = build_npcs()

        session = repo.create_session(player=player, world=world, npcs=npcs)
        loaded = repo.load_session(session.id)
        assert "guard" in loaded.npcs
        assert loaded.npcs["guard"].name == "Edric"
