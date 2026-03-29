# Development Conventions

## Purpose

This document defines engineering conventions for Structured Freedom, including
how human developers and AI coding agents should collaborate.

The goal is to keep implementation consistent, testable, and aligned with the
project's core idea: freeform input inside a constrained, persistent world.

## Core Engineering Rules

- The engine is authoritative over world state.
- AI outputs must never become canon without validation.
- Prefer simple, testable systems over clever abstractions.
- Preserve a clean separation between simulation, AI, persistence, and client
  code.
- Build for persistence from the start.
- Add tests alongside behavior, especially for rejection and validation paths.

## Programming Principles

These rules should guide implementation choices across the codebase.

- `KISS`: choose the simplest design that correctly solves the current problem
- `DRY`: avoid duplicated logic, but do not force abstractions too early
- `SRP`: keep modules and classes focused on one reason to change
- prefer composition over inheritance unless inheritance is clearly simpler
- make invalid states hard to represent
- favor explicit data flow over hidden side effects
- prefer pure functions in rules-heavy logic where practical
- optimize for readability and debugging over cleverness

Negative space programming is a good fit for this project.

That means:

- do not build systems before the MVP actually needs them
- do not introduce abstractions only because they might be useful later
- do not add provider/model routing complexity before more than one route exists
- do not create framework-heavy scaffolding without a real use case

The default bias should be:

- less code
- fewer moving parts
- clearer boundaries
- stronger tests

## Python Environment

- Use a local virtual environment in `.venv`.
- Do not rely on globally installed Python packages.
- Keep project dependencies explicit.
- Prefer reproducible local setup from a fresh checkout.

Expected local workflow:

1. Create `.venv`
2. Activate `.venv`
3. Install dependencies
4. Configure `.env`
5. Run tests before and after changes

## Configuration And Secrets

- Use `.env` for local configuration and secrets.
- Commit a `.env.example` with required variable names and safe placeholders.
- Never hardcode API keys, database URIs, or model credentials.
- Keep environment variable names stable and descriptive.
- Use typed Python config for application-level settings and validated loading.
- Keep `.env` small; do not turn it into the entire configuration model.

Examples of likely config areas:

- database connection
- cache connection
- LLM provider and endpoint
- default model
- logging level
- feature flags

## Logging

Logging is required, especially for debugging action resolution and AI behavior.

Conventions:

- use structured logs where possible
- use colored logs in local development
- keep logs readable from the terminal
- include request or action identifiers where useful
- log action interpretation, validation result, and persistence outcome
- never log secrets

Minimum areas that should be logged:

- incoming player action
- parsed intent
- validation decision
- state change summary
- AI request/response boundaries
- persistence success or failure

## AI Integration Conventions

- Prefer `DSPy` for structured AI interaction.
- Define explicit inputs and outputs for AI calls.
- Keep prompts and signatures versioned and testable.
- Do not scatter ad hoc prompt strings across the codebase.
- AI should produce structured proposals where possible.
- The rules engine must validate AI outputs before they affect game state.
- MVP should start with one model, even if the architecture allows more later.

Recommended pattern:

- player input enters the engine
- the engine builds structured context
- `DSPy` module parses intent or produces narration
- the engine validates the result
- only validated outcomes affect persistent state

## Testing Expectations

Tests are a core requirement, not optional polish.

Every meaningful gameplay system should include tests for:

- valid actions
- invalid actions
- persistence behavior
- regression cases

Special priority:

- rejecting impossible or world-breaking actions
- ensuring AI does not bypass simulation rules
- ensuring persistent state reloads correctly

Examples of required regression coverage:

- "I build a rocketship and fly away."
- "I take a bazooka out of my ass and fire at the king."
- any prompt that tries to invent unsupported items, powers, or world state

Expected behavior:

- the system rejects impossible actions clearly
- the system preserves world consistency
- the system does not silently turn absurd prompts into canon

## Collaboration Rules For AI Developers

AI coding agents working in this repository should follow these rules:

- read the relevant docs before making structural changes
- preserve the separation between engine logic and AI narration
- avoid introducing hidden magic or framework-heavy complexity too early
- prefer small, reviewable changes
- explain assumptions in code comments only where necessary
- add or update tests with behavior changes
- do not hardcode secrets or local machine paths
- do not bypass validation layers for convenience
- do not treat language-model output as trusted state

When implementing features:

- start from the MVP and current docs
- prefer explicit models and typed boundaries
- keep domain logic deterministic where possible
- make rejection behavior as intentional as success behavior

## Suggested Repository Conventions

These should guide early implementation:

- `src/` for application code
- `tests/` for automated tests
- `docs/` for design and planning documents
- `.env.example` for configuration template
- `.logs/` only if local file logging becomes necessary
- `.cache/` for any kind of caching like DSPy requests

Suggested logical separation inside the code:

- engine or simulation
- AI integration
- persistence
- API or transport
- client

## What To Prepare Before Implementation

A large amount of infrastructure is not required before the first code is
written, but a few decisions should be made early.

Recommended before starting:

- choose a Python version
- create `.venv`
- decide package management approach
- decide test runner
- create `.env.example`
- choose the primary database
- decide whether local development uses Docker or direct services
- decide one default AI provider and one default MVP model

## Database Recommendation

For this project, the recommended primary database is `PostgreSQL`, not
`MongoDB Atlas`.

Reason:

- the core world state is structured and relational
- consistency matters more than schema flexibility
- quests, inventory, NPC state, and world events are easier to keep correct in a
  relational system

Use `MongoDB` only if a document store later becomes useful for generated
artifacts or flexible content storage.

## Minimum Pre-Implementation Setup

Before the first serious implementation pass, have at least this ready:

- a local `.venv`
- a `.env.example`
- a local or hosted `PostgreSQL` database
- a test database strategy
- one logging setup for local development
- one baseline AI provider configuration
- one default MVP model configured

Practical options:

- local Postgres via Docker
- hosted Postgres such as Neon, Supabase, or Railway

For MVP speed, local Postgres or a simple hosted Postgres instance is enough.
You do not need MongoDB Atlas before starting.

## Nice To Have Early

- `pre-commit` hooks
- formatting and linting
- migration tooling
- a Makefile or task runner
- basic CI that runs tests

## Decision Bias

When in doubt:

- choose simpler architecture
- choose deterministic behavior over impressive behavior
- choose testability over speed of hacking
- choose explicit state over implicit AI memory
- choose less code over speculative abstractions
