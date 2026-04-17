# Sprint Backlog: Structured Freedom

> Last updated by: Project Manager

## Sprint 1 — Core Turn Loop (Backend)

Goal: A player can submit a turn via the API and receive a validated, narrated response backed by real AI interpretation.

### [EPIC-001] AI Layer

Outcome: DSPy modules interpret player intent, narrate outcomes, and generate NPC dialogue.

#### [STORY-001] Intent Interpreter
As a player, I want my natural language input to be understood as a structured game action.

Acceptance criteria:
- [ ] `IntentInterpreter` returns a `ParsedIntent` with `action_type`, `target`, `is_plausible`, `rejection_reason`
- [ ] Absurd inputs return `is_plausible=False` with a reason
- [ ] Common verbs (move, take, drop, use, examine, talk) are correctly classified

Tasks:
- [TASK-001] Create `src/structured_freedom/ai/intent.py` with DSPy `IntentInterpreter` — @developer — 1d
- [TASK-002] Create `src/structured_freedom/ai/provider.py` to configure DSPy LM from settings — @developer — 0.5d
- [TASK-003] Unit tests for intent classification — @qa — 0.5d

#### [STORY-002] Narrator
As a player, I want action outcomes narrated in atmospheric prose.

Acceptance criteria:
- [ ] `Narrator` accepts `ActionResult` + world context and returns prose string
- [ ] Narration correctly reflects success vs. rejection
- [ ] Narration does not invent facts not present in `ActionResult`

Tasks:
- [TASK-004] Create `src/structured_freedom/ai/narrator.py` — @developer — 0.5d
- [TASK-005] Unit tests for narrator output contracts — @qa — 0.5d

#### [STORY-003] NPC Dialogue
As a player, I want NPCs to respond in character with awareness of their state and memory.

Acceptance criteria:
- [ ] `NPCDialogue` accepts `NPCDialogueContext` + player speech and returns NPC response text
- [ ] Response is grounded in NPC role and disposition
- [ ] Response references recent memory entries when relevant

Tasks:
- [TASK-006] Create `src/structured_freedom/ai/dialogue.py` — @developer — 1d
- [TASK-007] Unit tests for dialogue module — @qa — 0.5d

---

### [EPIC-002] FastAPI Application

Outcome: Backend exposes a working REST API for session management and turn execution.

#### [STORY-004] Session Management
As a player, I want to create a game session and have my state tracked.

Acceptance criteria:
- [ ] `POST /api/sessions` returns a new session ID and initial world snapshot
- [ ] `GET /api/sessions/{id}` returns current session state

Tasks:
- [TASK-008] Create `src/structured_freedom/app/api/` with FastAPI app and session router — @developer — 1d
- [TASK-009] Create Pydantic response schemas in `app/api/schemas.py` — @developer — 0.5d
- [TASK-010] Integration test: create session returns valid state snapshot — @qa — 0.5d

#### [STORY-005] Turn Execution
As a player, I want to submit an action and receive a narrated outcome.

Acceptance criteria:
- [ ] `POST /api/sessions/{id}/turns` with `{"action": "..."}` returns `TurnResponse`
- [ ] `TurnResponse` contains `success`, `narration`, `state_snapshot`
- [ ] Invalid session ID returns 404
- [ ] Impossible actions return `success=false` with in-world narration

Tasks:
- [TASK-011] Update `app/turns.py` to full pipeline: load → AI intent → engine → persist → AI narrate — @developer — 2d
- [TASK-012] Create turn router in `app/api/` — @developer — 0.5d
- [TASK-013] Integration tests for turn execution — @qa — 1d

---

### [EPIC-003] Persistence

Outcome: Game state survives server restarts.

#### [STORY-006] ORM and Repository
As a developer, I want a clean persistence layer that separates domain models from database tables.

Acceptance criteria:
- [ ] SQLAlchemy ORM models for Session, TurnRecord
- [ ] `GameRepository` implements `create_session`, `load_session`, `save_session`, `append_turn`
- [ ] Repository tests pass with SQLite in-memory

Tasks:
- [TASK-014] Create `persistence/orm/models.py` with SQLAlchemy table definitions — @developer — 1d
- [TASK-015] Create `persistence/repositories/game_repo.py` — @developer — 1d
- [TASK-016] Alembic migration for initial schema — @devops — 0.5d
- [TASK-017] Repository unit tests — @qa — 1d

---

### [EPIC-004] World Content

Outcome: The MVP scenario is playable from start to finish.

#### [STORY-007] MVP Fixtures
As a player, I want to start in a believable village world with interactive NPCs and items.

Acceptance criteria:
- [ ] World contains 5 locations (village, tavern, market, gate, forest_edge)
- [ ] World contains at least 5 interactive items
- [ ] World contains 4 NPCs (innkeeper, guard, merchant, mysterious stranger)
- [ ] Guard blocks the gate north passage (world flag: `gate_north_blocked=True`)

Tasks:
- [TASK-018] Create `src/structured_freedom/world/fixtures.py` with MVP world content — @developer — 1d
- [TASK-019] Create `src/structured_freedom/world/scenario.py` with quest definitions — @developer — 0.5d
- [TASK-020] Smoke test: fixture loads without errors and passes world validators — @qa — 0.5d

---

## Sprint 2 — React Frontend

Goal: A player can play the full MVP scenario through the web UI.

### [EPIC-005] React Web Client

Outcome: Players interact with the game through a functional browser-based UI.

#### [STORY-008] Game Layout
As a player, I want a clear UI showing my location, inventory, and action log.

Acceptance criteria:
- [ ] LocationPanel shows current location name and description
- [ ] GameLog shows the last N turn narrations
- [ ] InventoryPanel shows current items held
- [ ] QuestPanel shows active and completed objectives
- [ ] ActionInput accepts free-form text and submits on Enter or button press

Tasks:
- [TASK-021] Scaffold Vite + React + TypeScript project in `frontend/` — @devops — 0.5d
- [TASK-022] Create TypeScript API types matching backend schemas — @developer — 0.5d
- [TASK-023] Create API client (`frontend/src/api/client.ts`) — @developer — 0.5d
- [TASK-024] Implement LocationPanel component — @developer — 0.5d
- [TASK-025] Implement GameLog component — @developer — 0.5d
- [TASK-026] Implement InventoryPanel and QuestPanel components — @developer — 0.5d
- [TASK-027] Implement ActionInput component — @developer — 0.5d
- [TASK-028] Wire App.tsx to API client with session lifecycle — @developer — 1d

#### [STORY-009] Loading and Error States
As a player, I want clear feedback while the AI is thinking and when things go wrong.

Acceptance criteria:
- [ ] Loading spinner shown while turn is processing
- [ ] Error messages shown when the API returns an error
- [ ] Input is disabled while processing to prevent double-submission

Tasks:
- [TASK-029] Add loading/error state handling to App.tsx — @developer — 0.5d

---

## Sprint 3 — Polish & Post-MVP

- [EPIC-006] Image generation via Replicate (Flux) — post-MVP
- [EPIC-007] Music generation via Suno API — post-MVP
- [EPIC-008] WebSocket streaming narration — post-MVP
- [EPIC-009] Story artifact ingestion tool — post-MVP
- [SPIKE-001] DSPy structured output evaluation with Ollama
- [SPIKE-002] WebSocket streaming feasibility
- [SPIKE-003] World artifact format specification
