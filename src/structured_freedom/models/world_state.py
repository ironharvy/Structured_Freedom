"""Aggregate world state that holds locations, items, and global flags."""

from __future__ import annotations

from pydantic import BaseModel, Field

from structured_freedom.models.item import Item
from structured_freedom.models.location import Location


class WorldState(BaseModel):
    """Top-level container for the canonical world state."""

    locations: dict[str, Location] = Field(default_factory=dict)
    items: dict[str, Item] = Field(default_factory=dict)
    flags: dict[str, bool] = Field(default_factory=dict)

    def get_flag(self, key: str, default: bool = False) -> bool:
        """Return the value of a world flag, or *default* if unset."""
        return self.flags.get(key, default)

    def set_flag(self, key: str, value: bool) -> None:
        """Set a world flag to *value*."""
        if not key:
            raise ValueError("Flag key must be a non-empty string")
        self.flags[key] = value

    def items_at(self, location_id: str) -> list[Item]:
        """Return every item whose ``location_id`` matches *location_id*."""
        return [item for item in self.items.values() if item.location_id == location_id]

    def move_item(self, item_id: str, destination_id: str | None) -> None:
        """Move an item to *destination_id* (``None`` removes it from the map)."""
        if item_id not in self.items:
            raise KeyError(f"Unknown item: {item_id!r}")
        self.items[item_id].location_id = destination_id
