"""Action result models for the MVP scaffold."""

from dataclasses import dataclass


@dataclass(slots=True)
class ActionResult:
    """Validated result returned by the engine."""

    success: bool
    message: str
