# Agent Workflow

## Purpose

This document defines how multiple AI coding agents should collaborate on
Structured Freedom.

The project may involve:

- local agents running on the same machine
- local agents using different tools
- remote agents such as Jules

The workflow must minimize merge conflicts, stale assumptions, and low-quality
large diffs.

## Core Rule

Parallel agents should collaborate through shared docs and git, not by blindly
editing the same files at the same time.

## Roles

### Human Lead

The human remains the final authority for:

- architecture
- prioritization
- merges
- acceptance of AI-generated work

### Coordinator Agent

Optional role.

Responsibilities:

- turn milestones into bounded tasks
- update `docs/tasks.md`
- keep task scope small and reviewable
- point workers to the right docs and decisions

This agent should not be the sole authority over architecture or acceptance.

### Worker Agents

Responsibilities:

- implement one task
- stay within assigned file scope
- add or update tests
- report assumptions, changed files, and verification

### Reviewer Agent

Optional role.

Responsibilities:

- review finished changes
- look for regressions, missing tests, and architecture drift
- avoid rewriting already acceptable work without cause

## Required Shared Context

Before taking a task, every agent should read:

- `README.md`
- `docs/mvp.md`
- `docs/architecture.md`
- `docs/development.md`
- `docs/decisions.md`
- the specific entry in `docs/tasks.md`

Agents should not rely on previous chat memory alone.

## Task Assignment Rules

- One task has one owner at a time.
- Each task must have a clear file scope.
- Each task must include acceptance criteria.
- If two tasks touch the same files, do them sequentially unless there is a very
  strong reason not to.
- If a task is too large for a clean review, split it first.

## Same-Machine Workflow

Some agents may run on the same machine and even target the same repository.

This is risky if they share one live working directory.

Preferred order of safety:

1. separate git worktrees
2. separate cloned folders
3. separate branches with serialized local execution
4. one shared folder with strict manual coordination

Recommended rule:

- if an agent will edit files, give it an isolated worktree or folder whenever
  possible

Why:

- reduces overwrite risk
- avoids editor temp file conflicts
- prevents one agent from reading half-finished work from another
- makes review and merge easier

## Shared-Folder Fallback Rules

If multiple agents must operate in the same folder:

- never assign overlapping file scopes
- keep tasks extremely small
- require agents to re-read touched files before editing
- merge one finished task at a time
- run tests after each merged change

This mode should be treated as fragile.

## Git Best Practices

Git discipline is essential for multi-agent work.

Rules:

- use one branch or worktree per task when possible
- keep commits focused on one logical change
- prefer small diffs
- do not mix refactors with behavior changes unless necessary
- do not let one agent silently rewrite another agent's area
- merge only after review and checks pass

Recommended flow:

1. claim task
2. create branch or worktree
3. implement task
4. run checks
5. submit for review
6. merge
7. update `docs/tasks.md`

## Review Requirements

Every completed task should report:

- files changed
- tests added or updated
- commands run
- assumptions made
- known limitations or follow-ups

Minimum checks before merge:

- `pytest`
- `ruff check .`

## Prompting Rules For Worker Agents

A worker task prompt should include:

- task id and title
- exact scope
- files allowed to change
- files that must not be changed
- acceptance criteria
- required tests
- architectural constraints

Good example:

- implement `T-004`
- only edit `src/structured_freedom/config/`, `src/structured_freedom/logging.py`, and related tests
- do not modify persistence or engine modules
- keep one-model MVP assumptions intact

## Good Task Shapes

Good:

- add initial SQLAlchemy models and migration setup
- implement CLI display of current location and inventory
- add regression tests for absurd invalid actions

Bad:

- build the backend
- implement the whole engine
- improve AI behavior

## Conflict Prevention

To reduce conflicts:

- use `docs/decisions.md` as architecture truth
- use `docs/tasks.md` as the task ledger
- avoid parallel edits to shared foundation files
- finish core infrastructure tasks before parallelizing feature work

High-conflict files should usually have serialized ownership:

- `pyproject.toml`
- central config modules
- shared database models
- shared engine orchestration modules

## Suggested Practical Setup

For this project, a pragmatic workflow is:

- one coordinator updates task docs
- one or more workers take isolated tasks
- one reviewer checks completed work
- the human lead decides what merges

Suggested early parallelization:

- one agent on persistence setup
- one agent on config/logging
- one agent on CLI improvements
- one agent on regression tests

Only do this in parallel if file scopes are clearly separated.

## Non-Negotiables

- small changes
- explicit task ownership
- tests with behavior changes
- no direct AI mutation of canonical state
- no large speculative refactors
- no same-file parallel editing unless absolutely necessary
