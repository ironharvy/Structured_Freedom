---
name: Agent Task
about: A task to be implemented by an AI coding agent
labels: agent-task
---

## Summary

<!-- What should be built or changed? Keep it specific. -->

## Requirements

<!-- Detailed requirements. Be explicit — agents follow instructions literally. -->

## Constraints

<!-- What the agent must NOT do. Examples: -->
<!-- - DO NOT add new dependencies -->
<!-- - DO NOT modify files outside src/structured_freedom/models/ -->
<!-- - DO NOT use SQLAlchemy — use Pydantic models only -->

## Files

<!-- Scope the work to specific files/directories. -->

- **May edit:**
- **Must not edit:**

## Tests

<!-- What tests must be written and where. -->

- [ ]

## Agent Checklist

The assigned agent MUST complete all of these steps:

- [ ] Read `AGENTS.md` before starting
- [ ] Create branch: `<agent>/<branch-name>` (exact name specified below)
- [ ] Implement the requirements above
- [ ] Run `ruff check .` — must pass
- [ ] Run `ruff format --check .` — must pass
- [ ] Run `pytest` — must pass
- [ ] Push the branch to the remote
- [ ] Create a pull request referencing this issue

## Assignment

- **Agent:** <!-- e.g. Cursor, Codex, Claude, Jules -->
- **Branch:** <!-- e.g. codex/player-model -->
