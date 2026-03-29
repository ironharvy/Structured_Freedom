"""Tests for the Location model and MVP map builder."""

import pytest
from pydantic import ValidationError

from structured_freedom.models.location import Location, build_mvp_map


class TestLocationCreation:
    def test_valid_location(self):
        loc = Location(id="tavern", name="Tavern", description="A cozy room.")
        assert loc.id == "tavern"
        assert loc.name == "Tavern"
        assert loc.description == "A cozy room."
        assert loc.connections == {}

    def test_default_description_is_empty(self):
        loc = Location(id="x", name="X")
        assert loc.description == ""

    def test_empty_name_rejected(self):
        with pytest.raises(ValidationError):
            Location(id="bad", name="")

    def test_connections_stored(self):
        loc = Location(id="a", name="A", connections={"north": "b", "east": "c"})
        assert loc.connections == {"north": "b", "east": "c"}


class TestLocationConnectivity:
    def test_connected_locations(self):
        loc = Location(id="a", name="A", connections={"north": "b", "east": "c"})
        assert loc.connected_locations() == {"b", "c"}

    def test_connected_locations_empty(self):
        loc = Location(id="a", name="A")
        assert loc.connected_locations() == set()

    def test_has_connection_true(self):
        loc = Location(id="a", name="A", connections={"north": "b"})
        assert loc.has_connection("north") is True

    def test_has_connection_false(self):
        loc = Location(id="a", name="A", connections={"north": "b"})
        assert loc.has_connection("south") is False

    def test_get_connection_exists(self):
        loc = Location(id="a", name="A", connections={"north": "b"})
        assert loc.get_connection("north") == "b"

    def test_get_connection_missing(self):
        loc = Location(id="a", name="A")
        assert loc.get_connection("north") is None


class TestMvpMap:
    def test_contains_five_locations(self):
        locations = build_mvp_map()
        assert len(locations) == 5
        assert set(locations.keys()) == {
            "village",
            "tavern",
            "market",
            "gate",
            "forest_edge",
        }

    def test_all_connections_bidirectional(self):
        locations = build_mvp_map()
        for loc_id, loc in locations.items():
            for direction, target_id in loc.connections.items():
                target = locations[target_id]
                reverse_targets = target.connected_locations()
                assert loc_id in reverse_targets, (
                    f"{loc_id} -> {target_id} via {direction} has no return path"
                )

    def test_village_is_hub(self):
        locations = build_mvp_map()
        village = locations["village"]
        assert village.connected_locations() == {"gate", "tavern", "market"}
