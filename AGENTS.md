# Multi-Agent Collaboration Guide

This repository is developed collaboratively by multiple AI agents (Claude, Codex, Cursor, Jules, and others) under human oversight. This file is a quick-start entrypoint. For detailed guidelines, see the docs listed below.

## Project Overview

**Structured Freedom** is an experimental AI-powered game engine for persistent, natural-language roleplaying. See `README.md` for the full vision and architecture direction.

## Essential Reading

Before picking up any work, read these in order:

1. **[docs/agent-workflow.md](docs/agent-workflow.md)** - Collaboration model, roles, conflict avoidance, review rules
2. **[docs/decisions.md](docs/decisions.md)** - Active project decisions (tech choices, scope, conventions)
4. **[docs/architecture.md](docs/architecture.md)** - System design, turn pipeline, state model
5. **[docs/development.md](docs/development.md)** - Engineering conventions, testing, coding standards
6. **[docs/mvp.md](docs/mvp.md)** - MVP scope and success criteria

## Ground Rules

1. **Never push directly to `main`.** All work goes through feature branches and pull requests.
2. **One agent, one branch.** Do not commit to another agent's active branch without coordination.
3. **PRs require human review** for architectural changes, new dependencies, or security-sensitive code.
4. **Read before you write.** Always check existing code and recent PRs before starting work to avoid conflicts.
5. **Small, focused PRs.** Each PR should address a single concern. Don't bundle unrelated changes.
6. **Tests are mandatory.** All new features and bug fixes must include tests.
7. **Don't break the build.** CI (ruff + pytest) must pass before merging.

## Branch Naming Convention

Use the following format: `<agent>/<description>`

| Agent   | Prefix      | Example                          |
|---------|-------------|----------------------------------|
| Claude  | `claude/`   | `claude/add-room-generator`      |
| Codex   | `codex/`    | `codex/fix-npc-dialogue`         |
| Cursor  | `cursor/`   | `cursor/refactor-world-state`    |
| Jules   | `jules/`    | `jules/add-quest-system`         |
| Human   | `feat/`     | `feat/manual-updates`            |

## Commit Message Format

```
<type>(<scope>): <short description>

<optional body>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `ci`, `chore`

## How to Pick Up Work

1. Check GitHub Issues for available tasks
2. Check open PRs to avoid duplicating effort
3. Assign yourself to the issue (or leave a comment) before starting
4. Create a branch following the naming convention
5. Do the work in small, testable increments
6. Open a PR with a clear description
7. Wait for CI to pass and human review

## Architecture Decisions

Major decisions are recorded in `docs/decisions.md`. Before making any of the following changes, create an issue or PR description explaining the rationale and wait for human approval:

- Adding new dependencies or frameworks
- Changing the tech stack or project structure
- Modifying CI/CD pipelines
- Altering database schemas
- Changing public APIs or interfaces
- Security-related changes

## Conflict Resolution

If two agents are working on overlapping areas:
- The agent who opened a PR first has priority
- The second agent should rebase on the first agent's branch or wait for merge
- When in doubt, create an issue to discuss the approach

## Communication

- Use **PR descriptions** and **issue comments** for async communication
- Tag `@ironharvy` for decisions that need human input
- Use clear, descriptive PR titles so the maintainer can review efficiently
