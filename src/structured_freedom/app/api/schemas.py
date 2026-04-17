"""Pydantic request/response schemas for the API."""

from __future__ import annotations

from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    player_name: str = "Traveller"


class StateSnapshot(BaseModel):
    location_id: str
    location_name: str
    location_description: str
    inventory: list[str]
    quests: dict[str, dict]
    turn_number: int


class SessionResponse(BaseModel):
    session_id: str
    state: StateSnapshot


class TurnRequest(BaseModel):
    action: str


class TurnResponse(BaseModel):
    success: bool
    narration: str
    state: StateSnapshot
