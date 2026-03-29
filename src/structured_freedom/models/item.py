"""Item model for interactive objects in the world."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Item(BaseModel):
    """An interactive object that can exist in a location or a player's inventory."""

    id: str
    name: str = Field(min_length=1)
    description: str = ""
    location_id: str | None = None
    takeable: bool = True
    usable: bool = False
