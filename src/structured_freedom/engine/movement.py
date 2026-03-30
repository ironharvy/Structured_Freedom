"""Movement system for the game engine."""

from structured_freedom.engine.actions import ActionResult
from structured_freedom.models.location import Location
from structured_freedom.models.player import Player


def move_player(
    player: Player,
    direction: str,
    locations: dict[str, Location],
) -> ActionResult:
    """Move a player in a direction if the destination exists and is connected.

    Args:
        player: The player to move.
        direction: The direction to move (e.g., "north", "south").
        locations: A mapping of location IDs to Location objects.

    Returns:
        ActionResult indicating success/failure and a descriptive message.
    """
    normalized_direction = direction.strip().lower()
    if not normalized_direction:
        return ActionResult(
            success=False,
            message="You must specify a direction to move.",
        )

    current_location_id = player.current_location
    if current_location_id not in locations:
        return ActionResult(
            success=False,
            message="Your current location no longer exists in the world.",
        )

    current_location = locations[current_location_id]

    if not current_location.has_connection(normalized_direction):
        return ActionResult(
            success=False,
            message=f"You cannot go {normalized_direction} from here.",
        )

    destination_id = current_location.get_connection(normalized_direction)

    if destination_id is None:
        return ActionResult(
            success=False,
            message=f"You cannot go {normalized_direction} from here.",
        )

    if destination_id not in locations:
        return ActionResult(
            success=False,
            message="That path leads nowhere.",
        )

    if destination_id == current_location_id:
        return ActionResult(
            success=False,
            message="You are already there.",
        )

    destination = locations[destination_id]
    player.move_to(destination_id)

    return ActionResult(
        success=True,
        message=f"You move {normalized_direction} to {destination.name}.",
    )
