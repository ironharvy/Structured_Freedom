# Decisions

## Purpose

This file records active project decisions so that human and AI contributors can
work from the same source of truth.

Keep entries short. When a decision changes, update the status and add the new
entry instead of silently rewriting history.

## Decision Template

```md
## D-000 Short Title

- Status: `active`
- Date: `YYYY-MM-DD`
- Decision: short statement
- Why:
  - reason
  - reason
- Notes:
  - optional implementation note
```

## Active Decisions

## D-001 MVP Starts Single-Player

- Status: `active`
- Date: `2026-03-28`
- Decision: The MVP is single-player first.
- Why:
  - it reduces scope and coordination cost
  - it lets the team prove the core gameplay loop before shared-world complexity
- Notes:
  - future direction remains co-op or shared multiplayer

## D-002 Python CLI First

- Status: `active`
- Date: `2026-03-28`
- Decision: The MVP client is a Python CLI, not a web UI.
- Why:
  - it keeps focus on engine behavior
  - it reduces frontend scope during early iteration
- Notes:
  - a web client can come later once the core loop is stable

## D-003 Canonical Store Is PostgreSQL

- Status: `active`
- Date: `2026-03-28`
- Decision: `PostgreSQL` is the primary database for MVP and canonical world state.
- Why:
  - world state is structured and relational
  - consistency matters more than schema flexibility
- Notes:
  - MongoDB is not required for MVP

## D-004 AI Provider Starts With Local Ollama

- Status: `active`
- Date: `2026-03-28`
- Decision: MVP uses local `Ollama` first.
- Why:
  - it is enough to validate the core AI-assisted loop
  - it keeps iteration local and inexpensive
- Notes:
  - architecture should still allow more providers later

## D-005 One Model For MVP

- Status: `active`
- Date: `2026-03-28`
- Decision: Use one default model for MVP.
- Why:
  - it avoids premature routing complexity
  - it keeps configuration and testing simpler
- Notes:
  - task-specific model routing can be added later in typed config

## D-006 DSPy Is Preferred For Structured AI Calls

- Status: `active`
- Date: `2026-03-28`
- Decision: Use `DSPy` as the default abstraction for structured AI interaction.
- Why:
  - it fits the need for explicit task boundaries
  - it supports structured inputs and outputs better than scattered raw prompts
- Notes:
  - AI outputs still require deterministic validation

## D-007 Small Reviewable Diffs Are Mandatory

- Status: `active`
- Date: `2026-03-28`
- Decision: Changes should be small and easy to review.
- Why:
  - this project will involve multiple AI agents in parallel
  - smaller diffs reduce merge conflicts and hidden regressions
- Notes:
  - large tasks should be split before implementation

## D-008 Prefer Isolated Workspaces For Parallel Agents

- Status: `active`
- Date: `2026-03-28`
- Decision: Parallel agents that edit code should prefer isolated folders, worktrees, or branches rather than one shared live workspace.
- Why:
  - several agents may run on the same machine
  - shared live edits in one folder create avoidable conflicts and stale state
- Notes:
  - same-folder parallel work should be treated as a fallback, not the default

## D-009 React Frontend Replaces CLI-First Decision

- Status: `active`
- Date: `2026-04-16`
- Decision: The primary client for MVP is a React/Vite/TypeScript web UI. D-002 (Python CLI first) is superseded.
- Why:
  - user confirmed React as the target frontend during intake
  - the core gameplay loop (location panel, action log, inventory) maps naturally to a web layout
  - the CLI is retained as a debug/development utility only
- Notes:
  - supersedes D-002
  - frontend lives in `frontend/` at repo root

## D-010 LiteLLM As Provider Abstraction For DSPy

- Status: `active`
- Date: `2026-04-16`
- Decision: All DSPy LM calls route through LiteLLM, which is already installed. Provider (Ollama, OpenAI, Anthropic) is set via `AI_PROVIDER` env var.
- Why:
  - LiteLLM is already in the venv
  - single switch to change providers without code changes
  - consistent interface for Ollama (local dev) and cloud providers (production)
- Notes:
  - default dev provider remains Ollama (D-004 still active for local dev)
  - production provider to be decided when cloud deployment is scoped

## D-011 FastAPI Added As Backend Framework

- Status: `active`
- Date: `2026-04-16`
- Decision: FastAPI + Uvicorn added as the HTTP layer. `fastapi` and `uvicorn[standard]` added to `pyproject.toml` dependencies.
- Why:
  - async-native, Pydantic v2-native, OpenAPI docs out of the box
  - already referenced in `docs/mvp.md` technical baseline
- Notes:
  - `httpx` added to dev dependencies for async test client
  - new dependencies require human review per AGENTS.md before merge
