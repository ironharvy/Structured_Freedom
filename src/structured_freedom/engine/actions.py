"""Action result and intent models for the engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ActionResult:
    """Validated result returned by the engine."""

    success: bool
    message: str
    state_changes: dict[str, Any] = field(default_factory=dict)
