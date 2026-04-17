"""DSPy module for interpreting player natural language into structured game intent."""

from __future__ import annotations

from typing import Literal

import dspy
from pydantic import BaseModel

ActionType = Literal["move", "take", "drop", "use", "examine", "talk", "custom", "invalid"]


class ParsedIntent(BaseModel):
    """Structured representation of a player action after AI interpretation."""

    action_type: ActionType
    target: str
    parameters: dict[str, str]
    is_plausible: bool
    rejection_reason: str


class _IntentSignature(dspy.Signature):
    """Parse a player's free-form action into a structured game command.

    You are the intent parser for a medieval fantasy text adventure.
    Classify the action and identify its target. Reject actions that are
    physically impossible in a low-fantasy medieval world (no magic, no
    modern technology, no teleportation unless the world explicitly allows it).
    """

    world_context: str = dspy.InputField(
        desc="Brief description of the player's current location, nearby NPCs, and visible items."
    )
    player_action: str = dspy.InputField(
        desc="The raw natural-language action the player typed."
    )

    action_type: str = dspy.OutputField(
        desc=(
            "One of: move, take, drop, use, examine, talk, custom, invalid. "
            "Use 'custom' for valid but non-standard actions (e.g. 'poop', 'sit down'). "
            "Use 'invalid' for physically impossible or world-breaking actions."
        )
    )
    target: str = dspy.OutputField(
        desc=(
            "The primary target of the action. For move: a direction (north/south/east/west). "
            "For take/drop/use/examine: an item name or 'location'. "
            "For talk: an NPC name. For custom/invalid: a brief noun phrase or 'none'."
        )
    )
    is_plausible: str = dspy.OutputField(
        desc="'true' if the action is physically possible in a medieval world, 'false' otherwise."
    )
    rejection_reason: str = dspy.OutputField(
        desc="If not plausible, a short in-world reason. Empty string if plausible."
    )


class IntentInterpreter(dspy.Module):
    """Interprets free-form player text into a structured ParsedIntent."""

    def __init__(self) -> None:
        self.predict = dspy.Predict(_IntentSignature)

    def forward(self, player_action: str, world_context: str) -> ParsedIntent:
        result = self.predict(
            world_context=world_context,
            player_action=player_action,
        )

        action_type = result.action_type.strip().lower()
        valid_types = {"move", "take", "drop", "use", "examine", "talk", "custom", "invalid"}
        if action_type not in valid_types:
            action_type = "custom"

        is_plausible = result.is_plausible.strip().lower() not in {"false", "no", "0"}

        return ParsedIntent(
            action_type=action_type,  # type: ignore[arg-type]
            target=result.target.strip().lower(),
            parameters={},
            is_plausible=is_plausible,
            rejection_reason=result.rejection_reason.strip(),
        )
