# Requirements: Structured Freedom

> Last updated by: Business Analyst
> Decision references: [DEC-0001], [DEC-0002], [DEC-0003], [DEC-0004], [DEC-0005], [DEC-0006], [DEC-0009]

## Functional Requirements

| ID | Priority | Description |
|----|----------|-------------|
| FR-001 | must-have | Player can start a new game session; system creates player state and loads the MVP world |
| FR-002 | must-have | Player can type any free-form natural language action |
| FR-003 | must-have | System interprets free-form input into a structured intent (action type, target, parameters) using an LLM |
| FR-004 | must-have | Engine validates the structured intent against canonical world state; physically impossible actions are rejected |
| FR-005 | must-have | On success, engine applies deterministic state changes (movement, item pickup, NPC state updates) |
| FR-006 | must-have | AI narrates the validated outcome in atmospheric prose; narrative does not alter canonical state |
| FR-007 | must-have | Player can move between connected locations |
| FR-008 | must-have | Player can take, drop, and use items |
| FR-009 | must-have | Player can examine locations, NPCs, and items to get descriptions |
| FR-010 | must-have | Player can talk to NPCs; NPCs respond using AI dialogue grounded in their role, state, and memory |
| FR-011 | must-have | NPCs have bounded memory (last N interactions) that influences their responses |
| FR-012 | must-have | The game world includes the MVP scenario: village, tavern, market, gate, forest edge |
| FR-013 | must-have | The MVP scenario contains 3–5 NPCs, a short quest, and a set of interactive items |
| FR-014 | must-have | Game state (player, world, NPCs, quests) persists across server restarts |
| FR-015 | must-have | World state is loaded from a canonical fixture at session start |
| FR-016 | must-have | Impossible or absurd actions (rocketships, teleportation, bazooka) are rejected with an in-world explanation |
| FR-017 | must-have | React web client displays: current location, action log, inventory, quest objectives |
| FR-018 | must-have | React web client accepts free-form text input and submits turns to the backend |
| FR-019 | should-have | Player can perform complex multi-part actions ("pick up the lantern and examine it") |
| FR-020 | should-have | Quest progression is tracked; completing objectives updates player state |
| FR-021 | should-have | NPC disposition can shift (friendly → hostile) based on player actions |
| FR-022 | nice-to-have | WebSocket transport for real-time response streaming |
| FR-023 | nice-to-have | Image generation via Replicate (Flux model) for locations and NPCs |
| FR-024 | nice-to-have | Music generation via Suno API for ambient atmosphere |

## Non-Functional Requirements

| ID | Category | Description |
|----|----------|-------------|
| NFR-001 | performance | Turn round-trip (excluding LLM call) < 50ms at p95 |
| NFR-002 | performance | LLM intent interpretation + narration: no hard SLA; progress indicator on frontend |
| NFR-003 | reliability | No LLM output should be able to mutate canonical world state directly |
| NFR-004 | reliability | Engine rejection must produce no state transition; world state is unchanged on invalid action |
| NFR-005 | testability | Engine rules must be testable without a live LLM (mock AI layer in tests) |
| NFR-006 | security | No authentication required for MVP (single-player, local deployment) |
| NFR-007 | maintainability | AI provider is swappable via config (Ollama ↔ OpenAI ↔ Anthropic) without code changes |
| NFR-008 | maintainability | DSPy modules are versioned and documented; prompts are not scattered ad hoc |
| NFR-009 | observability | Each turn logs: raw input, parsed intent, validation outcome, state changes, narration boundaries |

## Constraints

- No existing MUD framework; custom engine required
- Python 3.12, FastAPI backend
- React + Vite frontend (TypeScript)
- PostgreSQL for production; SQLite acceptable for local development
- DSPy for all structured AI calls
- LiteLLM as the provider abstraction layer (supports Ollama, OpenAI, Anthropic)
- AI layer must not directly mutate canonical state (engine is authoritative)
- MVP excludes: images, music, story generation integration, multiplayer

## Open Questions / Research Spikes

- [SPIKE-001] DSPy structured output reliability with local Ollama models — do we need ChainOfThought or is Predict sufficient for intent parsing?
- [SPIKE-002] WebSocket vs. HTTP long-poll for streaming narration — evaluate for post-MVP
- [SPIKE-003] How to load world artifacts (world bible, character sheets) into the fixture system — format and tooling
