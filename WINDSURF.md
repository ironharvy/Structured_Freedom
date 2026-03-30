# Windsurf Instructions

Read `AGENTS.md` first for shared conventions.

## Role

You are a collaborator on Structured Freedom, an AI-based MUD generator. Multiple AI agents work on this repo. Follow the coordination rules in AGENTS.md strictly.

## Environment Setup

Before writing any code, set up the project environment:

1. **Use Python 3.12** — this project requires `python >= 3.12` (see `pyproject.toml`). Use `python3.12` explicitly, not the system default which may be an older version.
2. **Create a virtual environment** in the project root:
   ```bash
   python3.12 -m venv .venv
   ```
3. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```
4. **Install dependencies** (including dev dependencies):
   ```bash
   pip install -e ".[dev]"
   ```
5. **Verify setup** before starting work:
   ```bash
   python --version  # must show 3.12.x
   ruff check src/ tests/
   pytest
   ```

Always run commands inside the activated `.venv`. Never install packages globally or use a Python version older than 3.12.

## Workflow

- Always create a feature branch with the `windsurf/` prefix
- Check open PRs and recent commits before starting work to avoid conflicts
- Write tests for all new code
- Keep PRs small and focused
- Run `ruff check src/ tests/` and `pytest` before committing

## Code Style

- Use clear, descriptive names
- Prefer simple, readable code over clever abstractions
- Follow existing patterns in the codebase

## When to Escalate

Create an issue or PR comment tagging `@ironharvy` before:
- Adding new dependencies
- Changing project structure
- Making architectural decisions
- Modifying CI/CD configuration
- Any security-sensitive changes

## Testing

- All new features must include tests
- Bug fixes must include a regression test
- Run the full test suite before pushing

## Task Suitability (Kimi K2.5)

Based on observed performance (PR #15), the Windsurf Kimi K2.5 model has
specific strengths and weaknesses that should guide task assignment.

### Strengths

- Writes clean, readable, well-structured code
- Produces thorough test suites with good edge case coverage
- Follows branch naming, commit message, and PR conventions reliably
- Handles well-specified, self-contained features correctly
- Good PR descriptions with clear summaries

### Weaknesses

- **Poor codebase discovery** — does not thoroughly explore existing modules
  before writing new code. Tends to create greenfield implementations even
  when existing patterns and utilities are available.
- **Misses architectural conventions** — may not pick up on validate/resolve
  separation, shared abstractions (e.g. `WorldState`), or module-level
  export patterns unless explicitly told.
- **Duplication risk** — can reimplement functionality that already exists
  in neighboring files.

### Assign

- Isolated, greenfield features in new directories/modules
- New test files for existing code
- Bug fixes with clear reproduction steps
- Documentation tasks
- Tasks where the issue specifies exact files to read and patterns to follow

### Avoid

- Tasks requiring integration with existing architectural patterns
- Extending or refactoring existing modules
- Work that depends on understanding cross-module relationships
- Features where the agent must discover and reuse existing abstractions

### Mitigation

When assigning integration-heavy tasks, the issue description **must**:
- List specific files the agent must read before writing code
- Name the patterns/abstractions to follow (e.g. "use the validate/resolve pattern in `world_validators.py`")
- Explicitly state "do not create new modules — extend the existing ones"
