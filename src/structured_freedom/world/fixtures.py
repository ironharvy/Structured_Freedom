"""MVP world content: locations, items, and NPCs for the village gate scenario."""

from __future__ import annotations

from structured_freedom.models.item import Item
from structured_freedom.models.location import Location
from structured_freedom.models.npc import NPC
from structured_freedom.models.world_state import WorldState


def build_locations() -> dict[str, Location]:
    return {
        "village": Location(
            id="village",
            name="Village Square",
            description=(
                "The heart of Ashford village. A worn stone well stands at the centre. "
                "Paths branch east toward the Rusty Lantern tavern, south toward the market, "
                "and north toward the village gate."
            ),
            connections={"north": "gate", "east": "tavern", "south": "market"},
        ),
        "tavern": Location(
            id="tavern",
            name="The Rusty Lantern",
            description=(
                "A low-ceilinged common room thick with woodsmoke and the smell of ale. "
                "Rough-hewn tables fill the floor. A staircase leads up to the rooms above. "
                "The door back to the village square is to the west."
            ),
            connections={"west": "village"},
        ),
        "market": Location(
            id="market",
            name="Market Stalls",
            description=(
                "A handful of canvas-covered stalls selling bread, rope, and curiosities. "
                "Most are half-empty today. The path back to the village square is north."
            ),
            connections={"north": "village"},
        ),
        "gate": Location(
            id="gate",
            name="Village Gate",
            description=(
                "A heavy oak gate marks the northern edge of Ashford. "
                "A guardhouse stands to one side. The road north leads into the forest. "
                "The village square is south."
            ),
            connections={"south": "village", "north": "forest_edge"},
        ),
        "forest_edge": Location(
            id="forest_edge",
            name="Forest Edge",
            description=(
                "Tall oaks press close on either side. The air is cooler here. "
                "Something glints in the undergrowth. The gate back to the village is south."
            ),
            connections={"south": "gate"},
        ),
    }


def build_items() -> dict[str, Item]:
    return {
        "lantern": Item(
            id="lantern",
            name="Rusty Lantern",
            description="A battered iron lantern. The glass is cracked but it still holds a flame.",
            location_id="tavern",
            takeable=True,
            usable=True,
        ),
        "knife": Item(
            id="knife",
            name="Paring Knife",
            description="A small kitchen knife left on a tavern table.",
            location_id="tavern",
            takeable=True,
            usable=True,
        ),
        "bread": Item(
            id="bread",
            name="Loaf of Bread",
            description="A dense round loaf, still slightly warm.",
            location_id="market",
            takeable=True,
            usable=True,
        ),
        "rope": Item(
            id="rope",
            name="Coil of Rope",
            description="Ten metres of sturdy hemp rope.",
            location_id="market",
            takeable=True,
            usable=True,
        ),
        "amulet": Item(
            id="amulet",
            name="Silver Amulet",
            description=(
                "A small silver amulet shaped like a crescent moon. "
                "It matches the description of the item stolen from the miller."
            ),
            location_id="forest_edge",
            takeable=True,
            usable=False,
        ),
        "well": Item(
            id="well",
            name="Stone Well",
            description="A deep stone well at the centre of the village square. Cold water shimmers below.",
            location_id="village",
            takeable=False,
            usable=True,
        ),
        "notice_board": Item(
            id="notice_board",
            name="Notice Board",
            description=(
                "A wooden board nailed to a post. A fresh notice reads: "
                "'By order of the headman — the north gate is closed until the theft from Aldric's mill is resolved.'"
            ),
            location_id="village",
            takeable=False,
            usable=False,
        ),
    }


def build_npcs() -> dict[str, NPC]:
    return {
        "innkeeper": NPC(
            id="innkeeper",
            name="Marta",
            role="innkeeper",
            description=(
                "A stout woman in her fifties with flour on her apron. "
                "She runs the Rusty Lantern with brisk efficiency."
            ),
            current_location="tavern",
            disposition="friendly",
            state={
                "knows_about_theft": "yes",
                "gossip_shared": "false",
            },
        ),
        "guard": NPC(
            id="guard",
            name="Edric",
            role="gate guard",
            description=(
                "A young guard in ill-fitting armour. He looks tired and a little nervous. "
                "He has been posted at the gate since the theft was discovered."
            ),
            current_location="gate",
            disposition="neutral",
            state={
                "gate_locked": "true",
                "bribeable": "false",
                "told_player_about_theft": "false",
            },
        ),
        "merchant": NPC(
            id="merchant",
            name="Oswin",
            role="market trader",
            description=(
                "A wiry man with sharp eyes who sells rope, bread, and other provisions. "
                "He is visibly nervous today."
            ),
            current_location="market",
            disposition="neutral",
            state={
                "saw_thief": "true",
                "willing_to_talk": "false",
            },
        ),
        "stranger": NPC(
            id="stranger",
            name="The Stranger",
            role="mysterious traveller",
            description=(
                "A cloaked figure nursing a drink alone in the corner of the tavern. "
                "Their face is hidden. They watch you with quiet interest."
            ),
            current_location="tavern",
            disposition="neutral",
            state={
                "knows_thief_identity": "true",
                "trust_level": "0",
            },
        ),
    }


def build_initial_flags() -> dict[str, bool]:
    return {
        "gate_north_blocked": True,
        "theft_resolved": False,
        "player_met_guard": False,
        "amulet_recovered": False,
    }


def build_world() -> WorldState:
    """Build the complete MVP world state from fixtures."""
    return WorldState(
        locations=build_locations(),
        items=build_items(),
        flags=build_initial_flags(),
    )
