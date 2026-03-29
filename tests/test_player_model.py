from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from structured_freedom.persistence.database import Base, create_db_engine
from structured_freedom.persistence.models import Player


def _session_factory() -> sessionmaker:
    engine = create_db_engine()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def test_player_model_persists_with_defaults() -> None:
    session_factory = _session_factory()

    with session_factory() as session:
        session.add(Player(name="Aria"))
        session.commit()

        player = session.scalars(select(Player).where(Player.name == "Aria")).one()

    assert player.id
    assert player.location == "village_square"
    assert player.objective == "Investigate the gate theft"


def test_player_model_supports_explicit_state() -> None:
    session_factory = _session_factory()

    with session_factory() as session:
        session.add(
            Player(
                name="Bram",
                location="tavern",
                objective="Ask the guard about the lock-down",
            )
        )
        session.commit()

        player = session.scalars(select(Player).where(Player.name == "Bram")).one()

    assert player.location == "tavern"
    assert player.objective == "Ask the guard about the lock-down"
