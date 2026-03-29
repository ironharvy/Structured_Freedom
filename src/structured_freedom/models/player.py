"""Player-facing domain models for the MVP."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PlayerStats(BaseModel):
    """Minimal player attributes for the MVP."""

    model_config = ConfigDict(validate_assignment=True)

    strength: int = Field(default=1, ge=0, le=10)
    perception: int = Field(default=1, ge=0, le=10)
    charisma: int = Field(default=1, ge=0, le=10)


class QuestState(BaseModel):
    """Minimal quest tracker for MVP objective progress."""

    model_config = ConfigDict(validate_assignment=True)

    quest_id: str = Field(min_length=1)
    active_objectives: list[str] = Field(default_factory=list)
    completed_objectives: list[str] = Field(default_factory=list)
    is_completed: bool = False

    @field_validator("active_objectives", "completed_objectives")
    @classmethod
    def validate_objectives(cls, objectives: list[str]) -> list[str]:
        """Reject blank objectives and duplicates within the same list."""
        cleaned = [objective.strip() for objective in objectives]

        if any(not objective for objective in cleaned):
            msg = "Objectives must not be blank."
            raise ValueError(msg)

        if len(set(cleaned)) != len(cleaned):
            msg = "Objectives must be unique."
            raise ValueError(msg)

        return cleaned

    @model_validator(mode="after")
    def validate_objective_overlap(self) -> QuestState:
        """Prevent an objective from being both active and completed."""
        overlap = set(self.active_objectives) & set(self.completed_objectives)
        if overlap:
            msg = "Objectives cannot be both active and completed."
            raise ValueError(msg)
        return self

    def add_objective(self, objective: str) -> None:
        """Track a new active objective."""
        normalized = objective.strip()
        if not normalized:
            msg = "Objective must not be blank."
            raise ValueError(msg)
        if normalized in self.completed_objectives:
            msg = f"Objective {normalized!r} is already completed."
            raise ValueError(msg)
        if normalized not in self.active_objectives:
            self.active_objectives.append(normalized)

    def complete_objective(self, objective: str) -> None:
        """Mark an active objective as completed."""
        normalized = objective.strip()
        if normalized not in self.active_objectives:
            msg = f"Objective {normalized!r} is not active."
            raise ValueError(msg)

        self.active_objectives.remove(normalized)
        self.completed_objectives.append(normalized)

        if not self.active_objectives:
            self.is_completed = True


class Player(BaseModel):
    """Persistence-agnostic player state."""

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    current_location: str = Field(min_length=1)
    description: str = Field(min_length=1)
    stats: PlayerStats = Field(default_factory=PlayerStats)
    inventory: list[str] = Field(default_factory=list)
    inventory_limit: int = Field(default=10, ge=1)
    quests: dict[str, QuestState] = Field(default_factory=dict)

    @field_validator("id", "name", "current_location", "description")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        """Normalize required string fields."""
        normalized = value.strip()
        if not normalized:
            msg = "Value must not be blank."
            raise ValueError(msg)
        return normalized

    @field_validator("inventory")
    @classmethod
    def validate_inventory(cls, inventory: list[str]) -> list[str]:
        """Keep inventory item identifiers normalized and unique."""
        cleaned = [item.strip() for item in inventory]

        if any(not item for item in cleaned):
            msg = "Inventory item ids must not be blank."
            raise ValueError(msg)

        if len(set(cleaned)) != len(cleaned):
            msg = "Inventory item ids must be unique."
            raise ValueError(msg)

        return cleaned

    @model_validator(mode="after")
    def validate_inventory_capacity(self) -> Player:
        """Ensure stored inventory fits within the configured limit."""
        if len(self.inventory) > self.inventory_limit:
            msg = "Inventory exceeds configured capacity."
            raise ValueError(msg)
        return self

    def has_item(self, item_id: str) -> bool:
        """Check whether the player currently holds an item."""
        return item_id.strip() in self.inventory

    def add_item(self, item_id: str) -> None:
        """Add an item to the inventory if capacity allows."""
        normalized = item_id.strip()
        if not normalized:
            msg = "Item id must not be blank."
            raise ValueError(msg)
        if normalized in self.inventory:
            msg = f"Item {normalized!r} is already in inventory."
            raise ValueError(msg)
        if len(self.inventory) >= self.inventory_limit:
            msg = "Inventory is full."
            raise ValueError(msg)

        self.inventory.append(normalized)

    def remove_item(self, item_id: str) -> None:
        """Remove an item from the inventory."""
        normalized = item_id.strip()
        if normalized not in self.inventory:
            msg = f"Item {normalized!r} is not in inventory."
            raise ValueError(msg)

        self.inventory.remove(normalized)

    def move_to(self, location_id: str) -> None:
        """Update the player's current location."""
        normalized = location_id.strip()
        if not normalized:
            msg = "Location id must not be blank."
            raise ValueError(msg)

        self.current_location = normalized

    def track_quest(self, quest_state: QuestState) -> None:
        """Add or replace a tracked quest state."""
        self.quests[quest_state.quest_id] = quest_state
