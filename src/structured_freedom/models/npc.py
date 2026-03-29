"""NPC-facing domain models for the MVP."""

from __future__ import annotations

from copy import deepcopy
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

type Disposition = Literal["neutral", "friendly", "hostile"]
type NPCStateValue = bool | str


class NPCMemoryEntry(BaseModel):
    """A single recent interaction summary for an NPC."""

    model_config = ConfigDict(validate_assignment=True)

    summary: str = Field(min_length=1)
    turn_number: int = Field(ge=0)

    @field_validator("summary")
    @classmethod
    def strip_summary(cls, value: str) -> str:
        """Normalize stored memory summaries."""
        normalized = value.strip()
        if not normalized:
            msg = "Summary must not be blank."
            raise ValueError(msg)
        return normalized


class NPCMemory(BaseModel):
    """Bounded recent interaction history for an NPC."""

    model_config = ConfigDict(validate_assignment=True)

    entries: list[NPCMemoryEntry] = Field(default_factory=list)
    max_entries: int = Field(default=10, ge=1, le=10)

    @model_validator(mode="after")
    def validate_capacity(self) -> NPCMemory:
        """Reject over-capacity persisted memory payloads."""
        if len(self.entries) > self.max_entries:
            msg = "Memory exceeds configured capacity."
            raise ValueError(msg)
        return self

    def add_entry(self, summary: str, turn_number: int) -> None:
        """Append a new interaction and evict the oldest entry if needed."""
        self.entries.append(NPCMemoryEntry(summary=summary, turn_number=turn_number))
        overflow = len(self.entries) - self.max_entries
        if overflow > 0:
            del self.entries[:overflow]


class NPCDialogueContext(BaseModel):
    """Read-only dialogue view derived from canonical NPC state."""

    model_config = ConfigDict(validate_assignment=True, frozen=True)

    name: str
    role: str
    disposition: Disposition
    state: dict[str, NPCStateValue] = Field(default_factory=dict)
    recent_memories: list[NPCMemoryEntry] = Field(default_factory=list)


class NPC(BaseModel):
    """Persistence-agnostic NPC state."""

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    role: str = Field(min_length=1)
    description: str = Field(min_length=1)
    current_location: str = Field(min_length=1)
    disposition: Disposition = "neutral"
    state: dict[str, NPCStateValue] = Field(default_factory=dict)
    memory: NPCMemory = Field(default_factory=NPCMemory)

    @field_validator("id", "name", "role", "description", "current_location")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        """Normalize required string fields."""
        normalized = value.strip()
        if not normalized:
            msg = "Value must not be blank."
            raise ValueError(msg)
        return normalized

    @field_validator("state")
    @classmethod
    def validate_state(
        cls, state: dict[str, NPCStateValue]
    ) -> dict[str, NPCStateValue]:
        """Keep state flag keys normalized and string values stripped."""
        normalized_state: dict[str, NPCStateValue] = {}
        for key, value in state.items():
            normalized_key = key.strip()
            if not normalized_key:
                msg = "State keys must not be blank."
                raise ValueError(msg)

            if isinstance(value, str):
                normalized_value = value.strip()
                if not normalized_value:
                    msg = "State string values must not be blank."
                    raise ValueError(msg)
                normalized_state[normalized_key] = normalized_value
                continue

            normalized_state[normalized_key] = value

        return normalized_state

    def set_state(self, key: str, value: NPCStateValue) -> None:
        """Update a mutable NPC state flag with validation."""
        normalized_key = key.strip()
        if not normalized_key:
            msg = "State keys must not be blank."
            raise ValueError(msg)

        normalized_value = value.strip() if isinstance(value, str) else value
        if isinstance(normalized_value, str) and not normalized_value:
            msg = "State string values must not be blank."
            raise ValueError(msg)

        updated_state = dict(self.state)
        updated_state[normalized_key] = normalized_value
        self.state = updated_state

    def get_state(
        self, key: str, default: NPCStateValue | None = None
    ) -> NPCStateValue | None:
        """Read an NPC state flag by name."""
        return self.state.get(key.strip(), default)

    def build_dialogue_context(self) -> NPCDialogueContext:
        """Construct the read-only dialogue payload from canonical NPC state."""
        return NPCDialogueContext(
            name=self.name,
            role=self.role,
            disposition=self.disposition,
            state=deepcopy(self.state),
            recent_memories=list(self.memory.entries),
        )
