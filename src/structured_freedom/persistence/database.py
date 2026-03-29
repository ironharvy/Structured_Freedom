"""Database bootstrap helpers."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from structured_freedom.config.settings import Settings, get_settings


class Base(DeclarativeBase):
    """Base SQLAlchemy declarative model."""


def create_db_engine(settings: Settings | None = None):
    """Create a SQLAlchemy engine from settings."""
    active_settings = settings or get_settings()
    return create_engine(active_settings.database_url, future=True)


def create_session_factory(settings: Settings | None = None):
    """Create a SQLAlchemy session factory."""
    engine = create_db_engine(settings)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
