"""DSPy module for generating atmospheric prose narration from action results."""

from __future__ import annotations

import dspy

from structured_freedom.engine.actions import ActionResult


class _NarrationSignature(dspy.Signature):
    """Generate atmospheric narration for a medieval fantasy text adventure.

    You are the narrator. Write in second person, present tense. Be vivid but
    concise (2–4 sentences). Do not invent facts not present in the action
    result or world context. If the action failed, explain why in-world.
    """

    world_context: str = dspy.InputField(
        desc="Current location description and relevant world details."
    )
    action_result_summary: str = dspy.InputField(
        desc="What happened: action type, target, success/failure, and the system message."
    )

    narration: str = dspy.OutputField(
        desc="Atmospheric prose narration in second person, present tense, 2–4 sentences."
    )


class Narrator(dspy.Module):
    """Generates atmospheric prose from a validated ActionResult."""

    def __init__(self) -> None:
        self.predict = dspy.Predict(_NarrationSignature)

    def forward(self, result: ActionResult, world_context: str) -> str:
        status = "succeeded" if result.success else "failed"
        summary = f"Action {status}. {result.message}"

        prediction = self.predict(
            world_context=world_context,
            action_result_summary=summary,
        )
        return prediction.narration.strip()
