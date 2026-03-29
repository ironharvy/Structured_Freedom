# MVP

## Goal

The MVP should prove that natural-language play can work inside a structured,
persistent game world.

A player should be able to enter a small world, describe actions in plain
language, and receive outcomes that are:

- understandable
- rule-consistent
- persistent
- narrated well enough to feel like play, not command entry

The system should feel approachable even for players with no MUD or tabletop
background.

## Core Product Statement

Build a single-player, server-authoritative prototype where the player explores
a small world, interacts with NPCs and objects using natural language, and
progresses through a short scenario while the game world remains consistent and
persistent.

## In Scope

### World

- one small playable area
- a few connected locations
- a small set of interactive objects
- a small set of world flags and persistent changes

Example:

- village
- tavern
- market
- gate
- nearby ruins or forest edge

### Player

- one player character
- basic stats or attributes
- inventory
- location
- quest or objective state

### NPCs

- 3 to 5 NPCs
- each NPC has a role, a small amount of state, and limited memory
- NPCs respond through AI-assisted dialogue grounded in world state

### Interaction

- natural-language input
- movement between locations
- inspect / observe
- talk to NPCs
- take / drop / use items
- simple quest progression
- basic checks such as locked access, missing items, social permission, or
  simple skill-based outcomes

### Engine Behavior

- intent parsing from player input into structured actions
- validation against actual world state
- deterministic state updates when an action is valid
- clear rejection when an action is not possible
- AI narration generated from validated outcomes only

### Persistence

- save player state
- save world state changes
- save quest progression
- save important NPC state
- load the same state after restart

### Client

- a minimal playable client
- Python CLI is the preferred MVP default
- text input for actions
- story log / response log
- visible current location
- visible inventory
- visible objective or quest state

A web UI can come later. The MVP should prioritize proving the gameplay loop
and engine constraints before investing in frontend work.

## Out Of Scope

- multiplayer
- co-op
- large world generation
- image generation
- music generation
- advanced combat systems
- crafting/economy simulation
- autonomous NPC society simulation
- modding/tools/editor support

These can be added later. They should not block the first playable slice.

## Core Gameplay Loop

1. The player types an action in natural language.
2. The backend interprets the intent.
3. The rules layer checks whether the action is legal and possible.
4. The world state updates if the action succeeds.
5. The AI narrates the validated result.
6. The result is persisted.
7. The client shows the updated world and history.

## Example Scenario

The MVP should include one short scenario that exercises the core systems.

Example setup:

- the village gate is restricted after a theft
- the player must learn what happened and decide how to proceed
- possible approaches include talking, investigating, trading, persuading,
  sneaking, or finding proof

This should support multiple valid approaches without requiring a large content
base.

## Technical Baseline

- Backend: Python + `FastAPI`
- Frontend: `React` + `Vite`
- Persistence: `PostgreSQL`
- Cache / jobs: `Redis` only if needed early
- Transport: start with HTTP; add `WebSockets` when realtime behavior justifies
  it

## Must-Have Rules For AI

- AI does not directly change canonical world state.
- AI only narrates or proposes outcomes after the engine validates them.
- The engine must reject actions that violate world logic.
- The system should prefer a clear failure over a misleading fabricated success.

## Test Requirements

Testing is part of the MVP, not a follow-up task.

The project needs tests that prove the engine can preserve world logic even when
the player writes absurd, impossible, or adversarial prompts.

### Key test categories

- intent parsing for common valid actions
- action validation against world state
- persistence and reload behavior
- quest progression consistency
- NPC interaction consistency
- rejection of impossible or world-breaking actions

### Examples of actions the system must handle correctly

- "I open the tavern door and walk inside."
- "I ask the guard why the gate is closed."
- "I take the lantern from the table."

### Examples of actions the system must reject or constrain

- "I build a rocketship and fly away."
- "I take a bazooka out of my ass and fire at the king."
- "I summon a dragon and order it to burn the town."
- "I teleport to the treasure room."

Expected behavior:

- the engine should not treat these as valid just because the language model can
  imagine them
- the response should explain why the action fails in terms of the world
- the world state should remain unchanged unless some supported subset of the
  action is actually legal

### Minimum automated test coverage

- unit tests for action validation rules
- unit tests for intent-to-action mapping
- integration tests for a small end-to-end scenario
- persistence tests for save/reload correctness
- regression tests for previously accepted invalid actions

## Success Criteria

The MVP is successful if:

- a new player can understand how to play without learning special commands
- common actions resolve consistently
- impossible actions are rejected consistently
- the world state persists across restarts
- the scenario is playable from start to finish
- the experience feels like a game system, not an unconstrained chatbot

## First Milestone After MVP

After the MVP works, the next step should likely be one of these:

- expand the single-player scenario into a stronger content slice
- add more systemic NPC behavior
- introduce co-op or shared-world foundations
- add richer presentation layers such as generated images or music
