"""MVP quest and scenario definitions for the village gate scenario."""

from __future__ import annotations

from structured_freedom.models.player import Player, PlayerStats, QuestState
from structured_freedom.world.fixtures import build_world

MAIN_QUEST_ID = "village_gate"


def build_main_quest() -> QuestState:
    return QuestState(
        quest_id=MAIN_QUEST_ID,
        active_objectives=[
            "Learn why the gate is closed",
            "Recover the stolen amulet",
            "Return the amulet to open the gate",
        ],
        completed_objectives=[],
        is_completed=False,
    )


def build_player(name: str = "Traveller") -> Player:
    quest = build_main_quest()
    player = Player(
        id="player",
        name=name,
        current_location="village",
        description="A wanderer of uncertain origin.",
        stats=PlayerStats(strength=3, perception=4, charisma=3),
        inventory=[],
        inventory_limit=10,
    )
    player.track_quest(quest)
    return player


def build_context_for_location(location_id: str) -> str:
    """Build a brief world context string for the AI modules."""
    world = build_world()
    location = world.locations.get(location_id)
    if not location:
        return f"An unknown place with id {location_id!r}."

    items_here = [item.name for item in world.items_at(location_id)]
    exits = list(location.connections.keys())

    parts = [f"You are in {location.name}. {location.description}"]
    if items_here:
        parts.append(f"You can see: {', '.join(items_here)}.")
    if exits:
        parts.append(f"Exits: {', '.join(exits)}.")
    return " ".join(parts)
