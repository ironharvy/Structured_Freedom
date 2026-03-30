"""Location model for the world map."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Location(BaseModel):
    """A discrete place in the game world that the player can visit."""

    id: str
    name: str = Field(min_length=1)
    description: str = ""
    connections: dict[str, str] = Field(default_factory=dict)

    def connected_locations(self) -> set[str]:
        """Return the set of location IDs reachable from here."""
        return set(self.connections.values())

    def has_connection(self, direction: str) -> bool:
        """Check whether *direction* leads somewhere."""
        return direction in self.connections

    def get_connection(self, direction: str) -> str | None:
        """Return the location ID for *direction*, or ``None``."""
        return self.connections.get(direction)


def build_mvp_map() -> dict[str, Location]:
    """Construct the five MVP locations with bidirectional connections.

    Layout::

        forest_edge
             |
            gate
             |
          village --- tavern
             |
           market
    """
    locations = {
        "village": Location(
            id="village",
            name="Village Square",
            description=(
                "The heart of a small village. Paths branch in every direction."
            ),
            connections={
                "north": "gate",
                "east": "tavern",
                "south": "market",
            },
        ),
        "tavern": Location(
            id="tavern",
            name="The Rusty Lantern",
            description="A cozy tavern filled with the smell of stew and wood smoke.",
            connections={"west": "village"},
        ),
        "market": Location(
            id="market",
            name="Market Stalls",
            description="A handful of stalls selling provisions and curiosities.",
            connections={"north": "village"},
        ),
        "gate": Location(
            id="gate",
            name="Village Gate",
            description="A heavy wooden gate marks the edge of the village.",
            connections={
                "south": "village",
                "north": "forest_edge",
            },
        ),
        "forest_edge": Location(
            id="forest_edge",
            name="Forest Edge",
            description="Tall trees loom ahead. The path back to the village is clear.",
            connections={"south": "gate"},
        ),
    }
    return locations
