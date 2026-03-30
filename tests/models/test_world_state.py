"""Tests for the WorldState model."""

import pytest

from structured_freedom.models.item import Item
from structured_freedom.models.location import build_mvp_map
from structured_freedom.models.world_state import WorldState


class TestWorldFlags:
    def test_get_flag_default(self):
        ws = WorldState()
        assert ws.get_flag("gate_locked") is False

    def test_get_flag_custom_default(self):
        ws = WorldState()
        assert ws.get_flag("gate_locked", default=True) is True

    def test_set_and_get_flag(self):
        ws = WorldState()
        ws.set_flag("gate_locked", True)
        assert ws.get_flag("gate_locked") is True

    def test_overwrite_flag(self):
        ws = WorldState(flags={"gate_locked": True})
        ws.set_flag("gate_locked", False)
        assert ws.get_flag("gate_locked") is False

    def test_set_flag_empty_key_rejected(self):
        ws = WorldState()
        with pytest.raises(ValueError, match="non-empty"):
            ws.set_flag("", True)


class TestItemQueries:
    @pytest.fixture()
    def populated_state(self) -> WorldState:
        return WorldState(
            items={
                "lantern": Item(id="lantern", name="Lantern", location_id="tavern"),
                "key": Item(id="key", name="Key", location_id="tavern"),
                "sword": Item(id="sword", name="Sword", location_id="market"),
                "coin": Item(id="coin", name="Gold Coin", location_id=None),
            },
        )

    def test_items_at_returns_matching(self, populated_state: WorldState):
        tavern_items = populated_state.items_at("tavern")
        ids = {i.id for i in tavern_items}
        assert ids == {"lantern", "key"}

    def test_items_at_empty_location(self, populated_state: WorldState):
        assert populated_state.items_at("gate") == []

    def test_items_at_excludes_inventory(self, populated_state: WorldState):
        tavern_items = populated_state.items_at("tavern")
        assert all(i.id != "coin" for i in tavern_items)


class TestMoveItem:
    def test_move_to_location(self):
        ws = WorldState(
            items={"key": Item(id="key", name="Key", location_id="tavern")},
        )
        ws.move_item("key", "market")
        assert ws.items["key"].location_id == "market"

    def test_move_to_none(self):
        ws = WorldState(
            items={"key": Item(id="key", name="Key", location_id="tavern")},
        )
        ws.move_item("key", None)
        assert ws.items["key"].location_id is None

    def test_move_unknown_item_raises(self):
        ws = WorldState()
        with pytest.raises(KeyError, match="ghost_item"):
            ws.move_item("ghost_item", "village")


class TestSerialization:
    def test_round_trip(self):
        original = WorldState(
            locations=build_mvp_map(),
            items={
                "lantern": Item(id="lantern", name="Lantern", location_id="tavern"),
            },
            flags={"gate_locked": True},
        )
        data = original.model_dump()
        restored = WorldState.model_validate(data)

        assert restored.locations.keys() == original.locations.keys()
        assert restored.items["lantern"].location_id == "tavern"
        assert restored.get_flag("gate_locked") is True

    def test_empty_state_round_trip(self):
        original = WorldState()
        data = original.model_dump()
        restored = WorldState.model_validate(data)
        assert restored.locations == {}
        assert restored.items == {}
        assert restored.flags == {}


class TestMvpIntegration:
    def test_build_state_with_mvp_map(self):
        ws = WorldState(
            locations=build_mvp_map(),
            items={
                "lantern": Item(id="lantern", name="Lantern", location_id="tavern"),
                "gate_key": Item(
                    id="gate_key",
                    name="Gate Key",
                    location_id="market",
                    usable=True,
                ),
            },
            flags={"gate_locked": True},
        )
        assert len(ws.locations) == 5
        assert ws.get_flag("gate_locked") is True
        assert len(ws.items_at("tavern")) == 1
        assert len(ws.items_at("market")) == 1
