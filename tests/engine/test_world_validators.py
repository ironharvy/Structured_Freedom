"""Tests for world-state-aware action validators."""

from __future__ import annotations

from structured_freedom.engine.world_validators import (
    resolve_drop,
    resolve_move,
    resolve_take,
    validate_drop,
    validate_move,
    validate_take,
    validate_use,
)
from structured_freedom.models import Item, Location, Player, WorldState

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _player(
    location: str = "village",
    inventory: list[str] | None = None,
    inventory_limit: int = 10,
) -> Player:
    return Player(
        id="player-1",
        name="Hero",
        current_location=location,
        description="A brave adventurer.",
        inventory=inventory or [],
        inventory_limit=inventory_limit,
    )


def _world(
    *,
    locations: dict[str, Location] | None = None,
    items: dict[str, Item] | None = None,
    flags: dict[str, bool] | None = None,
) -> WorldState:
    if locations is None:
        locations = {
            "village": Location(
                id="village",
                name="Village Square",
                connections={"north": "gate", "east": "tavern"},
            ),
            "gate": Location(
                id="gate",
                name="Village Gate",
                connections={"south": "village", "north": "forest_edge"},
            ),
            "tavern": Location(
                id="tavern",
                name="The Rusty Lantern",
                connections={"west": "village"},
            ),
            "forest_edge": Location(
                id="forest_edge",
                name="Forest Edge",
                connections={"south": "gate"},
            ),
        }
    return WorldState(
        locations=locations,
        items=items or {},
        flags=flags or {},
    )


# ===================================================================
# Move
# ===================================================================


class TestValidateMove:
    def test_succeeds_when_direction_exists_and_not_blocked(self) -> None:
        player = _player(location="village")
        world = _world()

        result = validate_move(player, world, "north")

        assert result.success is True
        assert "gate" in result.message

    def test_fails_when_direction_does_not_exist(self) -> None:
        player = _player(location="village")
        world = _world()

        result = validate_move(player, world, "west")

        assert result.success is False
        assert "no exit" in result.message.lower()

    def test_fails_when_player_location_unknown(self) -> None:
        player = _player(location="void")
        world = _world()

        result = validate_move(player, world, "north")

        assert result.success is False
        assert "void" in result.message

    def test_fails_when_world_flag_blocks_connection(self) -> None:
        player = _player(location="gate")
        world = _world(flags={"gate_north_blocked": True})

        result = validate_move(player, world, "north")

        assert result.success is False
        assert "blocked" in result.message.lower()

    def test_unblocked_flag_does_not_prevent_movement(self) -> None:
        """A flag set to False should not block."""
        player = _player(location="gate")
        world = _world(flags={"gate_north_blocked": False})

        result = validate_move(player, world, "north")

        assert result.success is True


class TestResolveMove:
    def test_updates_player_location(self) -> None:
        player = _player(location="village")
        world = _world()

        resolve_move(player, world, "north")

        assert player.current_location == "gate"


# ===================================================================
# Take
# ===================================================================


def _sword_at_village() -> dict[str, Item]:
    return {
        "sword": Item(
            id="sword",
            name="Iron Sword",
            location_id="village",
            takeable=True,
        ),
    }


class TestValidateTake:
    def test_succeeds_when_item_at_location_takeable_and_has_space(self) -> None:
        player = _player(location="village")
        world = _world(items=_sword_at_village())

        result = validate_take(player, world, "sword")

        assert result.success is True
        assert "Iron Sword" in result.message

    def test_fails_when_item_not_at_player_location(self) -> None:
        player = _player(location="tavern")
        world = _world(items=_sword_at_village())

        result = validate_take(player, world, "sword")

        assert result.success is False
        assert "not here" in result.message.lower()

    def test_fails_when_item_not_takeable(self) -> None:
        items = {
            "fountain": Item(
                id="fountain",
                name="Stone Fountain",
                location_id="village",
                takeable=False,
            ),
        }
        player = _player(location="village")
        world = _world(items=items)

        result = validate_take(player, world, "fountain")

        assert result.success is False
        assert "cannot be taken" in result.message.lower()

    def test_fails_when_inventory_full(self) -> None:
        player = _player(
            location="village",
            inventory=["a", "b"],
            inventory_limit=2,
        )
        world = _world(items=_sword_at_village())

        result = validate_take(player, world, "sword")

        assert result.success is False
        assert "full" in result.message.lower()

    def test_fails_when_item_id_unknown(self) -> None:
        player = _player(location="village")
        world = _world()

        result = validate_take(player, world, "nonexistent")

        assert result.success is False
        assert "unknown" in result.message.lower()


class TestResolveTake:
    def test_moves_item_to_inventory(self) -> None:
        player = _player(location="village")
        world = _world(items=_sword_at_village())

        resolve_take(player, world, "sword")

        assert "sword" in player.inventory
        assert world.items["sword"].location_id is None


# ===================================================================
# Drop
# ===================================================================


class TestValidateDrop:
    def test_succeeds_when_player_has_item(self) -> None:
        items = {
            "sword": Item(
                id="sword",
                name="Iron Sword",
                location_id=None,
            ),
        }
        player = _player(location="village", inventory=["sword"])
        world = _world(items=items)

        result = validate_drop(player, world, "sword")

        assert result.success is True
        assert "Iron Sword" in result.message

    def test_fails_when_player_does_not_have_item(self) -> None:
        items = {
            "sword": Item(
                id="sword",
                name="Iron Sword",
                location_id=None,
            ),
        }
        player = _player(location="village")
        world = _world(items=items)

        result = validate_drop(player, world, "sword")

        assert result.success is False
        assert "don't have" in result.message.lower()

    def test_fails_when_item_id_unknown_in_world(self) -> None:
        player = _player(location="village", inventory=["ghost_item"])
        world = _world()

        result = validate_drop(player, world, "ghost_item")

        assert result.success is False
        assert "unknown" in result.message.lower()


class TestResolveDrop:
    def test_moves_item_to_location(self) -> None:
        items = {
            "sword": Item(
                id="sword",
                name="Iron Sword",
                location_id=None,
            ),
        }
        player = _player(location="village", inventory=["sword"])
        world = _world(items=items)

        resolve_drop(player, world, "sword")

        assert "sword" not in player.inventory
        assert world.items["sword"].location_id == "village"


# ===================================================================
# Use
# ===================================================================


class TestValidateUse:
    def test_succeeds_when_player_has_usable_item(self) -> None:
        items = {
            "potion": Item(
                id="potion",
                name="Health Potion",
                location_id=None,
                usable=True,
            ),
        }
        player = _player(location="village", inventory=["potion"])
        world = _world(items=items)

        result = validate_use(player, world, "potion")

        assert result.success is True
        assert "Health Potion" in result.message

    def test_fails_when_player_does_not_have_item(self) -> None:
        items = {
            "potion": Item(
                id="potion",
                name="Health Potion",
                location_id=None,
                usable=True,
            ),
        }
        player = _player(location="village")
        world = _world(items=items)

        result = validate_use(player, world, "potion")

        assert result.success is False
        assert "don't have" in result.message.lower()

    def test_fails_when_item_not_usable(self) -> None:
        items = {
            "rock": Item(
                id="rock",
                name="Plain Rock",
                location_id=None,
                usable=False,
            ),
        }
        player = _player(location="village", inventory=["rock"])
        world = _world(items=items)

        result = validate_use(player, world, "rock")

        assert result.success is False
        assert "cannot be used" in result.message.lower()
