"""Smoke tests for world fixtures and scenario integrity."""


from structured_freedom.engine.world_validators import validate_move
from structured_freedom.world.fixtures import build_npcs, build_world
from structured_freedom.world.scenario import (
    MAIN_QUEST_ID,
    build_main_quest,
    build_player,
)


class TestWorldFixtures:
    def test_all_locations_present(self):
        world = build_world()
        expected = {"village", "tavern", "market", "gate", "forest_edge"}
        assert expected == set(world.locations.keys())

    def test_connections_are_bidirectional(self):
        world = build_world()
        for loc_id, location in world.locations.items():
            for _direction, dest_id in location.connections.items():
                dest = world.locations.get(dest_id)
                assert dest is not None, f"{loc_id} connects to unknown {dest_id!r}"
                assert dest_id in world.locations

    def test_gate_north_blocked_flag(self):
        world = build_world()
        assert world.get_flag("gate_north_blocked") is True

    def test_gate_north_blocked_prevents_movement(self):
        from structured_freedom.world.scenario import build_player
        world = build_world()
        player = build_player()
        player.move_to("gate")

        result = validate_move(player, world, "north")
        assert result.success is False
        assert "blocked" in result.message.lower()

    def test_items_have_valid_locations(self):
        world = build_world()
        for item_id, item in world.items.items():
            if item.location_id is not None:
                assert item.location_id in world.locations, (
                    f"Item {item_id!r} references unknown location {item.location_id!r}"
                )

    def test_npcs_have_valid_locations(self):
        world = build_world()
        npcs = build_npcs()
        for npc_id, npc in npcs.items():
            assert npc.current_location in world.locations, (
                f"NPC {npc_id!r} is in unknown location {npc.current_location!r}"
            )


class TestScenario:
    def test_player_starts_in_village(self):
        player = build_player()
        assert player.current_location == "village"

    def test_main_quest_has_objectives(self):
        quest = build_main_quest()
        assert quest.quest_id == MAIN_QUEST_ID
        assert len(quest.active_objectives) > 0
        assert not quest.is_completed

    def test_player_has_main_quest(self):
        player = build_player("Finn")
        assert MAIN_QUEST_ID in player.quests
