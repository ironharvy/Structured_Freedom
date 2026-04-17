"""Tests for intent interpretation contracts — no live LLM required."""

from unittest.mock import MagicMock

import dspy

from structured_freedom.ai.intent import IntentInterpreter, ParsedIntent


def _make_prediction(**kwargs):
    pred = MagicMock(spec=dspy.Prediction)
    for k, v in kwargs.items():
        setattr(pred, k, v)
    return pred


class TestIntentInterpreter:
    def _interpreter_with_mock(self, **prediction_kwargs) -> IntentInterpreter:
        interpreter = IntentInterpreter()
        interpreter.predict = MagicMock(return_value=_make_prediction(**prediction_kwargs))
        return interpreter

    def test_move_action_classified(self):
        interpreter = self._interpreter_with_mock(
            action_type="move",
            target="north",
            is_plausible="true",
            rejection_reason="",
        )
        result = interpreter.forward("go north", "You are at the village gate.")
        assert result.action_type == "move"
        assert result.target == "north"
        assert result.is_plausible is True

    def test_take_action_classified(self):
        interpreter = self._interpreter_with_mock(
            action_type="take",
            target="lantern",
            is_plausible="true",
            rejection_reason="",
        )
        result = interpreter.forward("pick up the lantern", "You see a lantern on the table.")
        assert result.action_type == "take"
        assert result.target == "lantern"

    def test_absurd_action_rejected(self):
        interpreter = self._interpreter_with_mock(
            action_type="invalid",
            target="rocketship",
            is_plausible="false",
            rejection_reason="There are no rocketships in this world.",
        )
        result = interpreter.forward(
            "I build a rocketship and fly away",
            "You are in the village square.",
        )
        assert result.is_plausible is False
        assert "rocketship" in result.rejection_reason.lower()

    def test_unknown_action_type_falls_back_to_custom(self):
        interpreter = self._interpreter_with_mock(
            action_type="weird_unknown_type_xyz",
            target="nothing",
            is_plausible="true",
            rejection_reason="",
        )
        result = interpreter.forward("do something odd", "You are somewhere.")
        assert result.action_type == "custom"

    def test_false_string_variants_treated_as_not_plausible(self):
        for false_val in ("false", "False", "FALSE", "no", "No", "0"):
            interpreter = self._interpreter_with_mock(
                action_type="invalid",
                target="none",
                is_plausible=false_val,
                rejection_reason="Not possible.",
            )
            result = interpreter.forward("teleport to the vault", "You are here.")
            assert result.is_plausible is False, f"Expected False for {false_val!r}"

    def test_result_is_parsed_intent(self):
        interpreter = self._interpreter_with_mock(
            action_type="examine",
            target="notice board",
            is_plausible="true",
            rejection_reason="",
        )
        result = interpreter.forward("look at the notice board", "There is a notice board here.")
        assert isinstance(result, ParsedIntent)
