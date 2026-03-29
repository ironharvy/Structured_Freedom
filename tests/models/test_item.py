"""Tests for the Item model."""

import pytest
from pydantic import ValidationError

from structured_freedom.models.item import Item


class TestItemCreation:
    def test_defaults(self):
        item = Item(id="lantern", name="Lantern")
        assert item.id == "lantern"
        assert item.name == "Lantern"
        assert item.description == ""
        assert item.location_id is None
        assert item.takeable is True
        assert item.usable is False

    def test_explicit_properties(self):
        item = Item(
            id="key",
            name="Rusty Key",
            description="An old iron key.",
            location_id="tavern",
            takeable=True,
            usable=True,
        )
        assert item.description == "An old iron key."
        assert item.location_id == "tavern"
        assert item.usable is True

    def test_empty_name_rejected(self):
        with pytest.raises(ValidationError):
            Item(id="bad", name="")


class TestItemPlacement:
    def test_item_at_location(self):
        item = Item(id="sword", name="Sword", location_id="market")
        assert item.location_id == "market"

    def test_item_in_inventory(self):
        item = Item(id="coin", name="Gold Coin", location_id=None)
        assert item.location_id is None

    def test_non_takeable_item(self):
        item = Item(id="well", name="Stone Well", takeable=False)
        assert item.takeable is False
