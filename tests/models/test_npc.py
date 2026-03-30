import pytest
from pydantic import ValidationError

from structured_freedom.models import NPC, NPCMemory, NPCMemoryEntry


def make_npc(**overrides: object) -> NPC:
    payload = {
        "id": "npc-guard-1",
        "name": "  Captain Mira  ",
        "role": "  guard  ",
        "description": "  The watch captain keeps a close eye on the square.  ",
        "current_location": "  village-gate  ",
    }
    payload.update(overrides)
    return NPC(**payload)


def test_npc_creation_supports_default_and_explicit_values() -> None:
    default_npc = make_npc()
    explicit_npc = make_npc(
        disposition="friendly",
        state={"has_given_quest": True, "rumor": "  saw movement by the gate  "},
        memory=NPCMemory(
            entries=[
                NPCMemoryEntry(summary="  Spoke with the player.  ", turn_number=2)
            ]
        ),
    )

    assert default_npc.name == "Captain Mira"
    assert default_npc.role == "guard"
    assert (
        default_npc.description == "The watch captain keeps a close eye on the square."
    )
    assert default_npc.current_location == "village-gate"
    assert default_npc.disposition == "neutral"
    assert default_npc.state == {}
    assert default_npc.memory.entries == []

    assert explicit_npc.disposition == "friendly"
    assert explicit_npc.state == {
        "has_given_quest": True,
        "rumor": "saw movement by the gate",
    }
    assert explicit_npc.memory.entries[0].summary == "Spoke with the player."


def test_npc_state_flag_read_write() -> None:
    npc = make_npc()

    npc.set_state("has_given_quest", True)
    npc.set_state(" rumor ", "  the theft happened at dusk  ")

    assert npc.get_state("has_given_quest") is True
    assert npc.get_state("rumor") == "the theft happened at dusk"
    assert npc.state == {
        "has_given_quest": True,
        "rumor": "the theft happened at dusk",
    }


def test_memory_addition_and_bounded_eviction() -> None:
    npc = make_npc(memory=NPCMemory(max_entries=3))

    for turn_number in range(1, 5):
        npc.memory.add_entry(f"Turn {turn_number}", turn_number)

    assert [entry.summary for entry in npc.memory.entries] == [
        "Turn 2",
        "Turn 3",
        "Turn 4",
    ]
    assert [entry.turn_number for entry in npc.memory.entries] == [2, 3, 4]


def test_dialogue_context_construction_from_npc_data() -> None:
    npc = make_npc(disposition="hostile")
    npc.set_state("is_aware_of_theft", True)
    npc.memory.add_entry("Warned the player away from the gate.", 7)

    context = npc.build_dialogue_context()

    assert context.name == "Captain Mira"
    assert context.role == "guard"
    assert context.disposition == "hostile"
    assert context.state == {"is_aware_of_theft": True}
    assert [entry.summary for entry in context.recent_memories] == [
        "Warned the player away from the gate."
    ]

    npc.set_state("is_aware_of_theft", False)

    assert context.state == {"is_aware_of_theft": True}


def test_npc_validation_rejects_blank_names_and_invalid_dispositions() -> None:
    with pytest.raises(ValidationError):
        make_npc(name="   ")

    with pytest.raises(ValidationError, match="neutral|friendly|hostile"):
        make_npc(disposition="curious")
