from structured_freedom.app.turns import run_turn


def test_valid_action_is_accepted() -> None:
    result = run_turn("I open the tavern door and walk inside.")

    assert result.success is True
    assert "accepted" in result.message.lower()


def test_absurd_action_is_rejected() -> None:
    result = run_turn("I build a rocketship and fly away.")

    assert result.success is False
    assert result.message == "That is not possible in this world."
