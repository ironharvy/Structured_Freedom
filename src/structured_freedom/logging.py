"""Logging setup for local development and tests."""

import logging

from rich.console import Console
from rich.logging import RichHandler


def configure_logging(level: str = "INFO") -> None:
    """Configure colored terminal logging."""
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(level.upper())

    console = Console(stderr=True)
    handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        show_path=False,
        markup=False,
    )
    handler.setLevel(level.upper())

    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
