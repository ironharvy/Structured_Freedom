# Architecture

## Purpose

This document defines the intended system architecture for Structured Freedom at
the MVP stage and the design constraints that should survive later growth.

The primary goal is to support natural-language play inside a deterministic,
persistent world where AI assists interpretation and narration without becoming
the source of truth.

## Architectural Principles

- The engine is authoritative over canonical state.
- AI is an assistant to the engine, not a replacement for it.
- Persistence is first-class.
- Rejection behavior matters as much as success behavior.
- The MVP should optimize for clarity and testability, not breadth.
- The system should allow future model/provider expansion without premature
  complexity.

## High-Level Shape

The architecture should be server-authoritative even though the MVP starts with
a Python CLI client.

At a high level:

- client submits natural-language actions
- application layer builds execution context
- AI layer helps interpret or narrate
- engine validates and resolves actions
- persistence layer stores canonical results
- client receives the final outcome

## Main Components

### Client

MVP decision:

- Python CLI client first

Responsibilities:

- collect player input
- display narration and system feedback
- show current location, inventory, and objective state
- remain thin and disposable

The client should not contain game rules or canonical state logic.

### Application Layer

This layer coordinates a turn from input to result.

Responsibilities:

- receive player action requests
- load necessary world and player context
- call AI services where appropriate
- invoke deterministic validation and resolution
- persist the outcome
- format the response returned to the client

This is orchestration code, not core simulation logic.

### Simulation Engine

This is the core of the system.

Responsibilities:

- define canonical world rules
- validate whether actions are possible
- resolve state transitions
- reject unsupported or impossible actions
- protect world consistency

This layer must remain deterministic as much as possible.

Examples of decisions that belong here:

- whether a door is locked
- whether the player has an item
- whether an NPC is present
- whether a claimed action is physically or fictionally possible in the world
- what state changes occur after a successful action

### AI Layer

The AI layer should be a bounded subsystem behind explicit interfaces.

MVP responsibilities:

- intent interpretation
- narration generation

Later responsibilities:

- NPC dialogue support
- summarization
- memory distillation
- story seeding

The AI layer must not directly mutate canonical state.

### Persistence Layer

Responsibilities:

- store canonical player and world state
- store quest and objective progression
- store event history
- load state needed for each turn
- support save/reload and test isolation

This layer should hide database-specific details from the engine.

## Turn Pipeline

The core turn loop should work like this:

1. The client submits a natural-language action.
2. The application layer loads current player and world context.
3. The AI intent interpreter converts the input into structured intent.
4. The engine validates the structured intent against actual world state.
5. If invalid, the engine returns a rejection result.
6. If valid, the engine resolves deterministic state changes.
7. The AI narration layer generates a response from the validated result.
8. The persistence layer stores the updated canonical state and event record.
9. The client receives the final result.

Important rule:

- AI may help interpret what the player means
- AI may help narrate what happened
- the engine decides what actually happened

## Handling Invalid Or Absurd Actions

This system must resist the normal failure mode of unconstrained LLM apps:
accepting impossible inputs because they are easy to improvise around.

Examples:

- "I build a rocketship and fly away."
- "I take a bazooka out of my ass and fire at the king."
- "I teleport into the vault."

Required behavior:

- the intent layer can classify these actions
- the engine must reject them if the world does not support them
- the narrator should explain the rejection in-world or systemically
- persistence should record no illegal state transition

This rejection path is a core feature, not an edge case.

## State Model

The canonical state should remain structured and explicit.

MVP state categories:

- player
- locations
- items
- NPCs
- quests or objectives
- world flags
- event history

Suggested conceptual entities:

- `Player`
- `Location`
- `Item`
- `Npc`
- `Quest`
- `WorldEvent`
- `ActionResult`

Generated narration should not be treated as canonical state. It is a derived
artifact attached to validated outcomes.

## Persistence Strategy

Recommended primary store:

- `PostgreSQL`

Recommended MVP usage:

- store canonical world state in relational tables
- store event history for debugging and replay
- keep schema explicit for inventory, locations, NPC state, and quest progress

Optional supporting stores later:

- `Redis` for cache or background jobs
- document storage for generated artifacts if needed
- object storage for media

The MVP does not require MongoDB Atlas.

## AI Provider Architecture

The system should support multiple providers eventually, but the MVP should
implement one provider and one model first.

Current MVP decision:

- start with local `Ollama`
- design interfaces so other providers can be added later

Provider abstraction should separate:

- model invocation
- prompt or signature definition
- task-level orchestration

The engine should not care whether the underlying provider is Ollama, OpenAI,
Anthropic, or something else.

## DSPy Role

`DSPy` should be the preferred way to structure AI interactions.

Recommended uses in MVP:

- intent extraction into structured action candidates
- narration generation from validated action results

Rules:

- keep DSPy modules task-specific
- prefer typed or schema-constrained outputs
- validate all outputs before use
- version prompts or signatures intentionally

Avoid:

- embedding large ad hoc prompts throughout the codebase
- letting DSPy modules bypass domain rules
- mixing narration concerns with simulation concerns

## Configuration Strategy

`.env` should hold environment-specific values and secrets, but it should not
become the whole configuration system.

Recommended pattern:

- `.env` stores environment variables and credentials
- application config code loads and validates them
- model/task mapping lives in typed config, not scattered string lookups

For MVP, one model is enough.

Suggested MVP approach:

- `.env` contains provider choice, base URL, and default model
- a Python config module loads these values
- later, task-specific model routing can move into structured config

This keeps the MVP simple while leaving room for later:

- separate intent and narration models
- per-environment overrides
- provider-specific defaults

## Suggested Code Boundaries

One reasonable early structure is:

- `src/config/`
- `src/engine/`
- `src/ai/`
- `src/persistence/`
- `src/app/`
- `src/client/`
- `tests/`

Responsibility split:

- `config`: typed settings and environment loading
- `engine`: rules, validation, world logic, state transitions
- `ai`: DSPy modules, provider clients, response shaping
- `persistence`: repositories, database models, migrations
- `app`: turn orchestration and service entry points
- `client`: Python CLI MVP interface

## Logging And Observability

The system should log the turn pipeline clearly.

Minimum logging per action:

- player action input
- parsed structured intent
- validation outcome
- applied state changes
- AI narration request and result boundaries
- persistence success or failure

Local development logs should be colored and readable. Production logging can be
more structured and less decorative later.

## Testing Strategy

Architecture must support testing from the start.

Priority test layers:

- unit tests for engine validation and rules
- unit tests for AI output parsing and contracts
- integration tests for turn execution
- persistence tests for save/reload behavior
- regression tests for impossible or world-breaking prompts

The most important invariant is:

- no AI-generated output should be able to bypass engine rules and become canon

## MVP Implementation Bias

At MVP stage, choose the simpler option when there is doubt:

- Python CLI before web client
- one AI provider before many providers
- one model before per-task model routing
- explicit state tables before flexible document-heavy storage
- deterministic rule checks before agentic autonomy

The architecture should remain extensible, but the MVP should not be burdened
by solving future complexity too early.
