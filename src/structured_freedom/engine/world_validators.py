"""World-state-aware action validators for the simulation engine.

Each ``validate_*`` function is **pure** — it inspects the current state and
returns an :class:`ActionResult` without mutating anything.  A companion
``resolve_*`` function applies the state changes after the caller confirms
the action was valid.

Flag convention for blocking movement:
    ``{location_id}_{direction}_blocked``
    e.g. ``gate_north_blocked`` prevents moving north from the gate.
"""

from __future__ import annotations

from structured_freedom.engine.actions import ActionResult
from structured_freedom.models import Item, Player, WorldState

# ---------------------------------------------------------------------------
# Move
# ---------------------------------------------------------------------------


def validate_move(player: Player, world: WorldState, direction: str) -> ActionResult:
    """Check whether *player* can move in *direction* from their current location."""
    if player.current_location not in world.locations:
        return ActionResult(
            success=False,
            message=(
                f"Current location {player.current_location!r} "
                "does not exist in the world."
            ),
        )

    location = world.locations[player.current_location]

    if not location.has_connection(direction):
        return ActionResult(
            success=False,
            message=f"There is no exit to the {direction} from {location.name}.",
        )

    flag_key = f"{player.current_location}_{direction}_blocked"
    if world.get_flag(flag_key):
        return ActionResult(
            success=False,
            message=f"The way {direction} is blocked.",
        )

    destination_id = location.get_connection(direction)
    return ActionResult(
        success=True,
        message=f"You move {direction} to {destination_id}.",
    )


def resolve_move(player: Player, world: WorldState, direction: str) -> None:
    """Apply a validated move: update the player's current location."""
    location = world.locations[player.current_location]
    destination_id = location.get_connection(direction)
    if destination_id is not None:
        player.move_to(destination_id)


# ---------------------------------------------------------------------------
# Take
# ---------------------------------------------------------------------------


def validate_take(player: Player, world: WorldState, item_id: str) -> ActionResult:
    """Check whether *player* can pick up *item_id*."""
    if item_id not in world.items:
        return ActionResult(
            success=False,
            message=f"Unknown item: {item_id!r}.",
        )

    item: Item = world.items[item_id]

    if item.location_id != player.current_location:
        return ActionResult(
            success=False,
            message=f"{item.name} is not here.",
        )

    if not item.takeable:
        return ActionResult(
            success=False,
            message=f"{item.name} cannot be taken.",
        )

    if len(player.inventory) >= player.inventory_limit:
        return ActionResult(
            success=False,
            message="Your inventory is full.",
        )

    return ActionResult(
        success=True,
        message=f"You take {item.name}.",
    )


def resolve_take(player: Player, world: WorldState, item_id: str) -> None:
    """Apply a validated take: move the item from the world to the player."""
    world.move_item(item_id, None)
    player.add_item(item_id)


# ---------------------------------------------------------------------------
# Drop
# ---------------------------------------------------------------------------


def validate_drop(player: Player, world: WorldState, item_id: str) -> ActionResult:
    """Check whether *player* can drop *item_id*."""
    if not player.has_item(item_id):
        return ActionResult(
            success=False,
            message="You don't have that item.",
        )

    if item_id not in world.items:
        return ActionResult(
            success=False,
            message=f"Unknown item: {item_id!r}.",
        )

    return ActionResult(
        success=True,
        message=f"You drop {world.items[item_id].name}.",
    )


def resolve_drop(player: Player, world: WorldState, item_id: str) -> None:
    """Apply a validated drop: move the item from inventory to the location."""
    player.remove_item(item_id)
    world.move_item(item_id, player.current_location)


# ---------------------------------------------------------------------------
# Use
# ---------------------------------------------------------------------------


def validate_use(player: Player, world: WorldState, item_id: str) -> ActionResult:
    """Check whether *player* can use *item_id*.

    Actual use effects are handled by a higher layer or AI narration;
    this validator only confirms the preconditions.
    """
    if not player.has_item(item_id):
        return ActionResult(
            success=False,
            message="You don't have that item.",
        )

    if item_id not in world.items:
        return ActionResult(
            success=False,
            message=f"Unknown item: {item_id!r}.",
        )

    item: Item = world.items[item_id]

    if not item.usable:
        return ActionResult(
            success=False,
            message=f"{item.name} cannot be used.",
        )

    return ActionResult(
        success=True,
        message=f"You use {item.name}.",
    )


# ---------------------------------------------------------------------------
# Examine
# ---------------------------------------------------------------------------


def validate_examine(
    player: Player, world: WorldState, target: str
) -> ActionResult:
    """Check whether *target* is examinable from the player's current location."""
    if target == "location" or target in {"here", "around", "room", ""}:
        location = world.locations.get(player.current_location)
        if location is None:
            return ActionResult(success=False, message="You seem to be nowhere.")
        return ActionResult(
            success=True,
            message=f"{location.name}: {location.description}",
            state_changes={"examined": "location", "location_id": player.current_location},
        )

    for item in world.items_at(player.current_location):
        if target in {item.id.lower(), item.name.lower()}:
            return ActionResult(
                success=True,
                message=f"{item.name}: {item.description}",
                state_changes={"examined": "item", "item_id": item.id},
            )
    for item_id in player.inventory:
        item = world.items.get(item_id)
        if item and target in {item.id.lower(), item.name.lower()}:
            return ActionResult(
                success=True,
                message=f"{item.name}: {item.description}",
                state_changes={"examined": "item", "item_id": item.id},
            )

    return ActionResult(
        success=False,
        message=f"You don't see {target!r} here.",
    )


# ---------------------------------------------------------------------------
# Talk
# ---------------------------------------------------------------------------


def validate_talk(
    player: Player, world: WorldState, npc_id: str, npcs: dict
) -> ActionResult:
    """Check whether the player can talk to an NPC at the current location."""
    npc = npcs.get(npc_id)
    if npc is None:
        npc = next(
            (n for n in npcs.values() if n.name.lower() == npc_id.lower()),
            None,
        )
    if npc is None:
        return ActionResult(
            success=False,
            message=f"There's nobody called {npc_id!r} here.",
        )
    if npc.current_location != player.current_location:
        return ActionResult(
            success=False,
            message=f"{npc.name} is not here.",
        )
    return ActionResult(
        success=True,
        message=f"You approach {npc.name}.",
        state_changes={"talk_target": npc.id},
    )
