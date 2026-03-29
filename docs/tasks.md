# Task Board

## Purpose

This file is the shared task board for human and AI contributors.

Every implementation task should be small, reviewable, and bounded by an
explicit file scope. Tasks should be claimed before work starts and updated when
their status changes.

## Status Legend

- `todo`
- `in_progress`
- `blocked`
- `review`
- `done`

## Task Template

Use this shape when adding new tasks:

```md
## T-000 Short Title

- Status: `todo`
- Owner: `unassigned`
- Scope: `src/...`, `tests/...`
- Depends on: `none`
- Acceptance:
  - clear acceptance criterion
  - required tests
- Notes:
  - useful constraint or context
```

## Current Tasks

## T-001 Database Models And Alembic Setup

- Status: `todo`
- Owner: `unassigned`
- Scope: `src/structured_freedom/persistence/`, `alembic/`, `tests/`
- Depends on: `none`
- Acceptance:
  - add initial SQLAlchemy models for core MVP entities
  - initialize Alembic
  - create first migration
  - add tests or verification for schema bootstrapping
- Notes:
  - keep models minimal
  - do not add speculative entities beyond MVP needs

## T-002 Turn Pipeline Domain Slice

- Status: `todo`
- Owner: `unassigned`
- Scope: `src/structured_freedom/engine/`, `src/structured_freedom/app/`, `tests/`
- Depends on: `T-001`
- Acceptance:
  - replace placeholder validation with a structured MVP action flow
  - support at least one real world-aware action
  - keep absurd-action rejection behavior covered by tests
- Notes:
  - engine remains authoritative
  - AI should not mutate state directly

## T-003 CLI Gameplay Loop

- Status: `todo`
- Owner: `unassigned`
- Scope: `src/structured_freedom/client/`, `tests/`
- Depends on: `T-002`
- Acceptance:
  - CLI can load a player session
  - CLI can submit actions through the turn pipeline
  - CLI displays location, response text, and basic state
- Notes:
  - keep the client thin
  - do not embed rules in the client

## T-004 Typed App Config And Startup

- Status: `todo`
- Owner: `unassigned`
- Scope: `src/structured_freedom/config/`, `src/structured_freedom/logging.py`, `tests/`
- Depends on: `none`
- Acceptance:
  - settings remain typed and validated
  - startup config supports current `.env` usage
  - logging remains colored locally and predictable in tests
- Notes:
  - keep `.env` small
  - do not introduce multi-model routing yet

## T-005 Regression Tests For Invalid Actions

- Status: `todo`
- Owner: `unassigned`
- Scope: `tests/`
- Depends on: `T-002`
- Acceptance:
  - add more rejection tests for impossible and adversarial prompts
  - verify no illegal state transition occurs on rejection
- Notes:
  - treat rejection behavior as a first-class feature

## Working Rules

- One task should have one clear owner at a time.
- Prefer tasks that can be reviewed in a small diff.
- Avoid assigning overlapping file scopes to parallel agents.
- If a task grows too large, split it before implementation.
