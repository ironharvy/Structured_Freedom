"""DSPy module for AI-driven NPC dialogue."""

from __future__ import annotations

import dspy

from structured_freedom.models.npc import NPCDialogueContext


class _DialogueSignature(dspy.Signature):
    """Generate an NPC's in-character response in a medieval fantasy text adventure.

    Stay in character. Ground the response in the NPC's role, disposition, and
    recent memories. Be concise (1–3 sentences). Do not break the fourth wall.
    If the NPC is hostile, be curt or threatening. If friendly, be warm.
    """

    npc_name: str = dspy.InputField(desc="The NPC's name.")
    npc_role: str = dspy.InputField(desc="The NPC's role in the world (e.g. 'innkeeper', 'guard').")
    npc_disposition: str = dspy.InputField(
        desc="Current disposition: 'friendly', 'neutral', or 'hostile'."
    )
    npc_state_summary: str = dspy.InputField(
        desc="Key facts about the NPC's current state (what they know, what they want)."
    )
    recent_memories: str = dspy.InputField(
        desc="Recent interactions with the player, comma-separated. Empty string if none."
    )
    player_speech: str = dspy.InputField(
        desc="What the player said or asked."
    )

    response: str = dspy.OutputField(
        desc="The NPC's in-character spoken response, 1–3 sentences."
    )
    mood_hint: str = dspy.OutputField(
        desc=(
            "Optional disposition shift hint: 'more_friendly', 'more_hostile', or 'unchanged'. "
            "Only shift if the player's speech clearly warrants it."
        )
    )


class NPCDialogue(dspy.Module):
    """Generates NPC dialogue grounded in character state and player interaction."""

    def __init__(self) -> None:
        self.predict = dspy.Predict(_DialogueSignature)

    def forward(self, context: NPCDialogueContext, player_speech: str) -> tuple[str, str]:
        """Return (npc_response_text, mood_hint)."""
        state_summary = "; ".join(
            f"{k}={v}" for k, v in context.state.items()
        ) or "nothing notable"

        memories_text = ", ".join(
            entry.summary for entry in context.recent_memories[-3:]
        ) if context.recent_memories else ""

        result = self.predict(
            npc_name=context.name,
            npc_role=context.role,
            npc_disposition=context.disposition,
            npc_state_summary=state_summary,
            recent_memories=memories_text,
            player_speech=player_speech,
        )

        mood_hint = result.mood_hint.strip().lower()
        if mood_hint not in {"more_friendly", "more_hostile", "unchanged"}:
            mood_hint = "unchanged"

        return result.response.strip(), mood_hint
