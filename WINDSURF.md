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
