"""SQLAlchemy ORM table definitions for Structured Freedom."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def _now() -> datetime:
    return datetime.now(UTC)


class SessionRow(Base):
    """Persisted game session: canonical player + world + NPC state."""

    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    player_json: Mapped[str] = mapped_column(Text, nullable=False)
    world_json: Mapped[str] = mapped_column(Text, nullable=False)
    npcs_json: Mapped[str] = mapped_column(Text, nullable=False)
    turn_number: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)


class TurnRow(Base):
    """Append-only record of a single executed turn."""

    __tablename__ = "turns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    turn_number: Mapped[int] = mapped_column(Integer, nullable=False)
    raw_input: Mapped[str] = mapped_column(Text, nullable=False)
    parsed_intent_json: Mapped[str] = mapped_column(Text, nullable=True)
    validation_success: Mapped[int] = mapped_column(Integer, nullable=False)
    state_changes_json: Mapped[str] = mapped_column(Text, nullable=True)
    narration: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
