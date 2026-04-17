# Architecture: Structured Freedom

> Last updated by: Tech Lead
> Decision references: [DEC-0001]–[DEC-0010]

## System Overview

Structured Freedom is a server-authoritative, single-player text adventure engine where an LLM assists with interpretation and narration but never controls canonical world state. The backend is a Python FastAPI service. The frontend is a React/Vite web client. The game engine is a deterministic rules layer that validates all actions before applying state changes.

The primary architectural principle: **the engine is authoritative, AI is advisory**. Any LLM output that would bypass engine validation is silently ignored or narrated as a failed action.

The turn pipeline is the system's critical path: raw player text → structured intent (AI) → engine validation → state mutation → prose narration (AI) → persistence → client response.

## Technology Stack

| Area | Choice | Rationale |
|------|--------|-----------|
| Language | Python 3.12 | Existing codebase, strong typing, async support |
| Web framework | FastAPI 0.115+ | Async-native, Pydantic-native, clean OpenAPI output |
| ASGI server | Uvicorn | Standard FastAPI runtime |
| AI orchestration | DSPy 2.6 | Typed signatures, structured outputs, provider-agnostic |
| AI provider abstraction | LiteLLM | Single interface to Ollama, OpenAI, Anthropic |
| Default LLM (dev) | Ollama (llama3.1:8b) | Local, free, fast enough for MVP validation |
| ORM | SQLAlchemy 2.0 | Already in stack, async-capable, explicit schema |
| Migrations | Alembic | Already installed, works with SQLAlchemy |
| Database (dev) | SQLite | Zero-config local development |
| Database (prod) | PostgreSQL 16 | Relational consistency for canonical state |
| Domain models | Pydantic v2 | Already in use, excellent validation |
| Testing | pytest | Already in use |
| Frontend framework | React 18 + Vite | Fast dev server, TypeScript support, minimal config |
| Frontend language | TypeScript | Type safety for API contract |
| HTTP client (frontend) | fetch / axios | Standard; no heavy framework needed |
| Linting | Ruff | Already in use |

> References: [DEC-0003], [DEC-0004], [DEC-0009], [DEC-0010]

## Component Breakdown

### Client (React/Vite)
Responsibility: render game state and submit player actions to the API.
Interfaces: REST `POST /api/turns`, `GET /api/sessions/{id}`.
Contains: LocationPanel, GameLog, ActionInput, InventoryPanel, QuestPanel.

### API Layer (FastAPI)
Responsibility: HTTP boundary — receive requests, delegate to app layer, return responses.
Interfaces: `POST /api/sessions`, `GET /api/sessions/{id}`, `POST /api/sessions/{id}/turns`.
Contains: session router, turn router, response schemas.

### App Layer (Turn Orchestrator)
Responsibility: coordinate a single turn from raw input to final result.
Interfaces: `run_turn(session_id, action_text)` → `TurnResult`.
Does not contain business rules or AI calls; it delegates to AI, Engine, and Persistence.

### AI Layer (DSPy Modules)
Responsibility: natural language ↔ structured data, constrained by explicit signatures.
Sub-components:
- `IntentInterpreter`: player text + world context → `ParsedIntent`
- `Narrator`: `ActionResult` + world context → prose string
- `NPCDialogue`: `NPCDialogueContext` + player speech → NPC response text
Interfaces: all modules accept typed inputs and return typed outputs; never receive mutable state.

### Simulation Engine
Responsibility: validate intents against world state and apply deterministic state transitions.
Interfaces: `validate_*(player, world, ...)` → `ActionResult`; `resolve_*(player, world, ...)` → None.
Already implemented for: move, take, drop, use. Needs: examine, talk, custom action routing.

### Persistence Layer
Responsibility: save and load canonical game state (player, world, NPCs, quests).
Sub-components:
- `ORM models`: SQLAlchemy table definitions
- `Repository`: `GameRepository` with load/save per entity
- `database.py`: engine + session factory
Interfaces: `GameRepository.load_session(id)`, `GameRepository.save_session(session)`.

### World / Fixtures
Responsibility: define the canonical MVP world content.
Sub-components:
- `fixtures.py`: locations, items, NPCs, initial world state for MVP scenario
- `scenario.py`: quest definitions and initial world flags for the village gate scenario

## Data Model

### Session
Top-level container: player state + world state + NPCs for one playthrough.
Fields: `id`, `player`, `world`, `npcs: dict[str, NPC]`, `turn_number`, `created_at`, `updated_at`.

### Player (existing)
Fields: `id`, `name`, `current_location`, `stats`, `inventory`, `quests`.

### WorldState (existing)
Fields: `locations: dict[str, Location]`, `items: dict[str, Item]`, `flags: dict[str, bool]`.

### Location (existing)
Fields: `id`, `name`, `description`, `connections: dict[str, str]`.

### Item (existing)
Fields: `id`, `name`, `description`, `location_id`, `takeable`, `usable`.

### NPC (existing)
Fields: `id`, `name`, `role`, `description`, `current_location`, `disposition`, `state`, `memory`.

### TurnRecord
Append-only event log entry per turn.
Fields: `id`, `session_id`, `turn_number`, `raw_input`, `parsed_intent`, `validation_success`, `state_changes`, `narration`, `created_at`.

## Turn Pipeline

```
1. Client  → POST /api/sessions/{id}/turns  { "action": "..." }
2. API     → TurnOrchestrator.run_turn(session_id, action_text)
3. App     → load Session from repository
4. AI      → IntentInterpreter.parse(action_text, world_context) → ParsedIntent
5. Engine  → validate_*(player, world, intent) → ActionResult
           → if invalid: skip to step 8
6. Engine  → resolve_*(player, world, intent) → mutate state
7. Persist → repository.save_session(session)
8. AI      → Narrator.narrate(action_result, world_context) → prose
9. Persist → repository.append_turn_record(turn)
10. API    → return TurnResponse { success, narration, state_snapshot }
```

## API Design

Base path: `/api`
Auth: none (MVP)
Content-type: `application/json`

```
POST   /api/sessions                → create new session, returns session_id + initial state
GET    /api/sessions/{id}           → get current session state
POST   /api/sessions/{id}/turns     → execute a turn, returns TurnResponse
GET    /api/sessions/{id}/turns     → turn history
```

Response shapes are defined as Pydantic models in `app/api/schemas.py`.

## Coding Standards

- All new modules in `src/structured_freedom/`
- DSPy modules live in `src/structured_freedom/ai/`
- ORM models live in `src/structured_freedom/persistence/orm/`
- Repositories live in `src/structured_freedom/persistence/repositories/`
- World content lives in `src/structured_freedom/world/`
- FastAPI app and routers live in `src/structured_freedom/app/`
- No raw LLM prompts outside DSPy signatures
- Engine functions remain pure (no I/O, no AI calls)
- All public functions have type annotations
- Test files mirror source structure under `tests/`

## Infrastructure

### Project Structure
```
structured_freedom/
├── src/structured_freedom/
│   ├── ai/             # DSPy modules
│   ├── app/            # FastAPI app + turn orchestrator
│   ├── client/         # CLI (keep for debugging)
│   ├── config/         # Settings
│   ├── engine/         # Deterministic rules
│   ├── models/         # Pydantic domain models
│   ├── persistence/    # ORM + repositories
│   └── world/          # Fixtures + scenario content
├── frontend/           # React/Vite web client
│   ├── src/
│   │   ├── api/        # API client
│   │   ├── components/ # UI components
│   │   └── types/      # TypeScript types
│   └── package.json
├── alembic/            # Database migrations
├── docs/
└── tests/
```

### CI/CD Pipeline
Stages: ruff lint → pytest → (frontend: npm ci + tsc + vitest)

### Containerization
Dockerfile: multi-stage, Python backend + static frontend build. Not required for MVP local dev.

## Open Questions
- SPIKE-001: DSPy structured output reliability with local Ollama — test before committing to ChainOfThought vs Predict
- SPIKE-002: WebSocket streaming for narration (post-MVP)
- SPIKE-003: World artifact ingestion format
