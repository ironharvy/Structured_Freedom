import pytest
from pydantic import ValidationError

from structured_freedom.models import Player, PlayerStats, QuestState


def make_player(**overrides: object) -> Player:
    payload = {
        "id": "player-1",
        "name": "Aria",
        "current_location": "village-square",
        "description": "A curious traveler investigating the gate theft.",
    }
    payload.update(overrides)
    return Player(**payload)


def test_player_creation_normalizes_fields() -> None:
    player = make_player(
        name="  Aria  ",
        current_location="  market  ",
        description="  A watchful investigator.  ",
        stats=PlayerStats(strength=2, perception=4, charisma=3),
    )

    assert player.name == "Aria"
    assert player.current_location == "market"
    assert player.description == "A watchful investigator."
    assert player.stats.perception == 4


def test_player_requires_non_blank_fields() -> None:
    with pytest.raises(ValidationError):
        make_player(name="   ")


def test_inventory_add_remove_and_check() -> None:
    player = make_player(inventory_limit=2)

    player.add_item("lantern")
    player.add_item("guard-note")

    assert player.has_item("lantern") is True
    assert player.inventory == ["lantern", "guard-note"]

    player.remove_item("lantern")

    assert player.has_item("lantern") is False
    assert player.inventory == ["guard-note"]


def test_inventory_rejects_duplicates_and_overflow() -> None:
    player = make_player(inventory_limit=1)
    player.add_item("lantern")

    with pytest.raises(ValueError, match="already in inventory"):
        player.add_item("lantern")

    with pytest.raises(ValueError, match="Inventory is full"):
        player.add_item("gate-key")


def test_player_moves_between_locations() -> None:
    player = make_player()

    player.move_to("tavern")

    assert player.current_location == "tavern"


def test_quest_state_tracks_progress_and_completion() -> None:
    quest = QuestState(
        quest_id="gate-theft",
        active_objectives=["speak to the guard", "search the market"],
    )

    quest.complete_objective("speak to the guard")

    assert quest.active_objectives == ["search the market"]
    assert quest.completed_objectives == ["speak to the guard"]
    assert quest.is_completed is False

    quest.complete_objective("search the market")

    assert quest.is_completed is True


def test_player_tracks_quests() -> None:
    player = make_player()
    quest = QuestState(quest_id="gate-theft", active_objectives=["inspect the gate"])

    player.track_quest(quest)

    assert player.quests["gate-theft"] == quest


def test_quest_state_rejects_overlapping_objectives() -> None:
    with pytest.raises(ValidationError, match="both active and completed"):
        QuestState(
            quest_id="gate-theft",
            active_objectives=["inspect the gate"],
            completed_objectives=["inspect the gate"],
        )
