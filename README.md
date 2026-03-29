# Structured Freedom

Structured Freedom is an experimental AI-powered game engine for persistent,
natural-language roleplaying.

The project combines the systemic reliability of classic MUDs with AI-driven
interpretation and narration. Players should be able to act in plain language
while the world remains consistent, fair, and persistent.

The design goal is not to build a niche tool only for MUD or tabletop players.
It should feel approachable even to someone with no MUD or TRPG background.

## Vision

Structured Freedom aims to make freeform interaction work inside a structured
simulation:

- players express actions in natural language
- the engine resolves what is actually possible
- AI interprets intent and narrates outcomes
- the world state stays authoritative and persistent

AI is also expected to support higher-level systems such as story generation,
NPC behavior, images, music, and other content layers. Those systems should
extend the engine, not replace its rules.

## Design Principles

- The engine owns canonical world state.
- AI can interpret, propose, and narrate, but should not change canon without
  validation.
- Player freedom should come from expressive input, not from bypassing rules.
- The game should be readable and intuitive for newcomers.
- Persistence matters from the beginning.

## Scope

Initial target:

- single-player first
- persistent world state
- natural-language actions
- AI-assisted narration and interpretation

Future direction:

- shared multiplayer or co-op worlds
- richer NPC systems
- generated media as optional supporting layers

## Architecture Direction

This project should use a client-server architecture.

The server should remain authoritative over simulation, persistence, and AI
orchestration. The client should focus on the player experience.

Recommended starting point:

- Backend: Python + `FastAPI`
- Frontend: JavaScript + `React` + `Vite`
- Realtime transport: `WebSockets`
- Background jobs: `Celery` or a simpler queue if needed

Why this direction:

- Python is a good fit for simulation and AI integration.
- React is a safe default for a stateful UI with room to grow.
- Client-server architecture keeps persistence and rules enforcement in one
  place.

## Persistence

Persistence is a core requirement, not an add-on.

Recommended baseline:

- `PostgreSQL` for canonical game state
- `Redis` for cache, locks, and job coordination
- object storage for generated media
- `MongoDB` only if a separate document store becomes useful for flexible
  generated content

`PostgreSQL` is the best default source of truth because this project will need
consistent updates across world state, inventory, quests, NPCs, and event
history.

## Core Loop

1. The player submits a natural-language action.
2. The engine parses intent and checks the current world state.
3. The rules system resolves what happens.
4. AI narrates the validated outcome.
5. The result is stored as part of the persistent world.

## Project Status

Structured Freedom is currently in the concept and planning stage.

The next milestone is to define a first playable vertical slice with:

- a minimal world model
- one core gameplay loop
- a simple action resolution pipeline
- persistent saves
- a basic UI for play and history

## Notes On Existing Frameworks

There is no obvious Python MUD framework that cleanly matches this vision out of
the box.

`Evennia` is worth studying as a reference, but a custom backend may be the
better fit if the project needs a strict boundary between simulation and AI
interpretation.
