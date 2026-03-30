"""Tests for the movement system."""

from structured_freedom.engine.movement import move_player
from structured_freedom.models.location import Location, build_mvp_map
from structured_freedom.models.player import Player


def make_player(location: str = "village") -> Player:
    """Create a test player at the specified location."""
    return Player(
        id="player-1",
        name="Aria",
        current_location=location,
        description="A curious traveler.",
    )


class TestValidMovement:
    def test_move_updates_player_location(self):
        locations = build_mvp_map()
        player = make_player("village")

        result = move_player(player, "east", locations)

        assert result.success is True
        assert player.current_location == "tavern"
        assert "the rusty lantern" in result.message.lower()

    def test_move_updates_location_case_insensitive(self):
        locations = build_mvp_map()
        player = make_player("village")

        result = move_player(player, "EAST", locations)

        assert result.success is True
        assert player.current_location == "tavern"

    def test_move_across_multiple_hops(self):
        locations = build_mvp_map()
        player = make_player("village")

        # Village -> Gate -> Forest Edge
        result1 = move_player(player, "north", locations)
        assert result1.success is True
        assert player.current_location == "gate"

        result2 = move_player(player, "north", locations)
        assert result2.success is True
        assert player.current_location == "forest_edge"


class TestInvalidMovement:
    def test_move_to_nonexistent_location_rejected(self):
        locations = {
            "village": Location(
                id="village",
                name="Village",
                connections={"north": "nonexistent"},
            ),
        }
        player = make_player("village")
        original_location = player.current_location

        result = move_player(player, "north", locations)

        assert result.success is False
        assert player.current_location == original_location
        assert "nowhere" in result.message.lower()

    def test_move_to_unconnected_location_rejected(self):
        locations = build_mvp_map()
        player = make_player("village")
        original_location = player.current_location

        # Village has no "west" connection - this should fail
        result = move_player(player, "west", locations)

        assert result.success is False
        assert player.current_location == original_location
        assert "cannot go" in result.message.lower()

    def test_move_when_already_at_destination(self):
        # Create a location that connects to itself (edge case)
        locations = {
            "village": Location(
                id="village",
                name="Village",
                connections={"circle": "village"},
            ),
        }
        player = make_player("village")
        original_location = player.current_location

        result = move_player(player, "circle", locations)

        assert result.success is False
        assert player.current_location == original_location
        assert "already there" in result.message.lower()


class TestEdgeCases:
    def test_empty_direction_rejected(self):
        locations = build_mvp_map()
        player = make_player("village")
        original_location = player.current_location

        result = move_player(player, "", locations)

        assert result.success is False
        assert player.current_location == original_location
        assert "specify a direction" in result.message.lower()

    def test_whitespace_direction_rejected(self):
        locations = build_mvp_map()
        player = make_player("village")
        original_location = player.current_location

        result = move_player(player, "   ", locations)

        assert result.success is False
        assert player.current_location == original_location

    def test_invalid_direction_rejected(self):
        locations = build_mvp_map()
        player = make_player("village")
        original_location = player.current_location

        result = move_player(player, "up", locations)

        assert result.success is False
        assert player.current_location == original_location
        assert "cannot go" in result.message.lower()

    def test_player_location_unchanged_after_rejected_move(self):
        locations = build_mvp_map()
        player = make_player("village")
        original_location = player.current_location

        # Try multiple invalid moves
        move_player(player, "west", locations)
        move_player(player, "up", locations)
        move_player(player, "down", locations)

        assert player.current_location == original_location

    def test_current_location_not_in_world(self):
        locations = build_mvp_map()
        player = make_player("nonexistent-start")

        result = move_player(player, "north", locations)

        assert result.success is False
        assert "no longer exists" in result.message.lower()
