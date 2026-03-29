"""Simple action validation for the MVP scaffold."""

from structured_freedom.engine.actions import ActionResult

ABSURD_PATTERNS = (
    "rocketship",
    "bazooka",
    "teleport",
    "summon a dragon",
)


def validate_player_action(action_text: str) -> ActionResult:
    """Validate a raw player action against basic MVP constraints."""
    normalized = action_text.strip().lower()

    if not normalized:
        return ActionResult(success=False, message="You need to do something.")

    if any(pattern in normalized for pattern in ABSURD_PATTERNS):
        return ActionResult(
            success=False,
            message="That is not possible in this world.",
        )

    return ActionResult(
        success=True,
        message="Action accepted for further resolution.",
    )
