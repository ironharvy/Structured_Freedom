"""Turn orchestration for the MVP scaffold."""

import logging

from structured_freedom.engine.actions import ActionResult
from structured_freedom.engine.validator import validate_player_action

logger = logging.getLogger(__name__)


def run_turn(action_text: str) -> ActionResult:
    """Execute a minimal turn pipeline."""
    logger.info("player_action=%r", action_text)
    result = validate_player_action(action_text)
    logger.info("validation_success=%s message=%r", result.success, result.message)
    return result

