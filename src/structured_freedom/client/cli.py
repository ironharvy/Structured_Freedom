"""Minimal CLI client for the MVP scaffold."""

from structured_freedom.app.turns import run_turn
from structured_freedom.config.settings import get_settings
from structured_freedom.logging import configure_logging


def main() -> None:
    """Run a simple CLI loop."""
    settings = get_settings()
    configure_logging(settings.log_level)

    print("Structured Freedom CLI")
    print("Type an action, or 'quit' to exit.")

    while True:
        try:
            action_text = input("> ").strip()
        except EOFError:
            print()
            break

        if action_text.lower() in {"quit", "exit"}:
            break

        result = run_turn(action_text)
        print(result.message)


if __name__ == "__main__":
    main()
