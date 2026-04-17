"""Database bootstrap helpers."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from structured_freedom.config.settings import Settings, get_settings
from structured_freedom.persistence.orm.models import Base


def create_db_engine(settings: Settings | None = None):
    """Create a SQLAlchemy engine from settings."""
    active_settings = settings or get_settings()
    connect_args = {}
    if "sqlite" in active_settings.database_url:
        connect_args["check_same_thread"] = False
    return create_engine(
        active_settings.database_url,
        future=True,
        connect_args=connect_args,
    )


def create_session_factory(settings: Settings | None = None):
    """Create a SQLAlchemy session factory."""
    engine = create_db_engine(settings)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db(settings: Settings | None = None) -> None:
    """Create all tables if they don't exist."""
    engine = create_db_engine(settings)
    Base.metadata.create_all(engine)
