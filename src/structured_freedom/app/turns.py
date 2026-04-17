"""Full turn pipeline: intent → validation → state mutation → narration → persistence."""

from __future__ import annotations

import json
import logging

from structured_freedom.ai.dialogue import NPCDialogue
from structured_freedom.ai.intent import IntentInterpreter
from structured_freedom.ai.narrator import Narrator
from structured_freedom.engine.actions import ActionResult
from structured_freedom.engine.validator import validate_player_action
from structured_freedom.engine.world_validators import (
    resolve_drop,
    resolve_move,
    resolve_take,
    validate_drop,
    validate_examine,
    validate_move,
    validate_take,
    validate_talk,
    validate_use,
)

logger = logging.getLogger(__name__)


def run_turn(action_text: str) -> ActionResult:
    """Thin wrapper for backward-compatible CLI use (no DB, no AI)."""
    logger.info("player_action=%r", action_text)
    result = validate_player_action(action_text)
    logger.info("validation_success=%s message=%r", result.success, result.message)
    return result


def _build_world_context(session) -> str:  # type: ignore[return]
    from structured_freedom.persistence.repositories.game_repo import GameSession

    if not isinstance(session, GameSession):
        return "Unknown location."

    world = session.world
    player = session.player
    location = world.locations.get(player.current_location)
    if not location:
        return "Unknown location."

    items_here = [item.name for item in world.items_at(player.current_location)]
    npcs_here = [
        n.name for n in session.npcs.values()
        if n.current_location == player.current_location
    ]
    exits = list(location.connections.keys())

    parts = [f"You are in {location.name}. {location.description}"]
    if items_here:
        parts.append(f"Visible items: {', '.join(items_here)}.")
    if npcs_here:
        parts.append(f"People here: {', '.join(npcs_here)}.")
    if exits:
        parts.append(f"Exits: {', '.join(exits)}.")
    return " ".join(parts)


def _dispatch_intent(intent, session) -> ActionResult:
    """Route a parsed intent to the appropriate engine validator/resolver."""
    player = session.player
    world = session.world

    if intent.action_type == "move":
        result = validate_move(player, world, intent.target)
        if result.success:
            resolve_move(player, world, intent.target)
        return result

    if intent.action_type == "take":
        result = validate_take(player, world, intent.target)
        if result.success:
            resolve_take(player, world, intent.target)
        return result

    if intent.action_type == "drop":
        result = validate_drop(player, world, intent.target)
        if result.success:
            resolve_drop(player, world, intent.target)
        return result

    if intent.action_type == "use":
        return validate_use(player, world, intent.target)

    if intent.action_type == "examine":
        return validate_examine(player, world, intent.target)

    if intent.action_type == "talk":
        return validate_talk(player, world, intent.target, session.npcs)

    if intent.action_type == "custom":
        return ActionResult(
            success=True,
            message=f"You attempt to {intent.target}.",
        )

    return ActionResult(
        success=False,
        message=intent.rejection_reason or "That is not possible in this world.",
    )


def run_turn_full(
    action_text: str,
    session,
    repo,
    use_ai: bool = True,
) -> dict:
    """Execute a complete turn with AI, engine, persistence, and narration."""
    logger.info("session=%s turn=%d input=%r", session.id, session.turn_number, action_text)

    world_context = _build_world_context(session)
    parsed_intent = None
    npc_response: str | None = None

    if use_ai:
        try:
            interpreter = IntentInterpreter()
            parsed_intent = interpreter.forward(
                player_action=action_text,
                world_context=world_context,
            )
            logger.info(
                "intent=%s target=%s plausible=%s",
                parsed_intent.action_type,
                parsed_intent.target,
                parsed_intent.is_plausible,
            )
        except Exception:
            logger.exception("Intent interpretation failed; falling back to basic validator.")

    if parsed_intent is None:
        result = validate_player_action(action_text)
    elif not parsed_intent.is_plausible:
        result = ActionResult(
            success=False,
            message=parsed_intent.rejection_reason or "That is not possible in this world.",
        )
    else:
        result = _dispatch_intent(parsed_intent, session)

    narration = result.message

    if use_ai:
        try:
            if result.success and parsed_intent and parsed_intent.action_type == "talk":
                npc_id = result.state_changes.get("talk_target", "")
                npc = session.npcs.get(npc_id)
                if npc:
                    ctx = npc.build_dialogue_context()
                    npc_response, mood_hint = NPCDialogue().forward(ctx, action_text)
                    if mood_hint == "more_friendly" and npc.disposition == "neutral":
                        npc.disposition = "friendly"
                    elif mood_hint == "more_hostile" and npc.disposition == "neutral":
                        npc.disposition = "hostile"
                    npc.memory.add_entry(
                        summary=f"Player said: {action_text[:80]}",
                        turn_number=session.turn_number,
                    )
                    narration = npc_response
            else:
                narration = Narrator().forward(result, world_context)
        except Exception:
            logger.exception("Narration/dialogue failed; using engine message.")

    session.turn_number += 1
    repo.save_session(session)
    repo.append_turn(
        session_id=session.id,
        turn_number=session.turn_number,
        raw_input=action_text,
        parsed_intent_json=parsed_intent.model_dump_json() if parsed_intent else None,
        validation_success=result.success,
        state_changes_json=json.dumps(result.state_changes),
        narration=narration,
    )

    location = session.world.locations.get(session.player.current_location)
    return {
        "success": result.success,
        "narration": narration,
        "state_snapshot": {
            "location_id": session.player.current_location,
            "location_name": location.name if location else "",
            "location_description": location.description if location else "",
            "inventory": session.player.inventory,
            "quests": {
                qid: {
                    "active": qs.active_objectives,
                    "completed": qs.completed_objectives,
                    "done": qs.is_completed,
                }
                for qid, qs in session.player.quests.items()
            },
            "turn_number": session.turn_number,
        },
    }
