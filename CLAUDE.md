# Claude Code Instructions

Read `AGENTS.md` first for shared conventions.

## Role

You are a collaborator on Structured Freedom, an AI-based MUD generator. Multiple AI agents work on this repo. Follow the coordination rules in AGENTS.md strictly.

## Workflow

- Always create a feature branch with the `claude/` prefix
- Check open PRs and recent commits before starting work to avoid conflicts
- Write tests for all new code
- Keep PRs small and focused
- Run linting and tests before committing

## Code Style

- Use clear, descriptive names
- Prefer simple, readable code over clever abstractions
- Add comments only where the logic isn't self-evident
- Follow existing patterns in the codebase

## When to Escalate

Tag `@ironharvy` or ask the user before:
- Adding new dependencies
- Changing project structure
- Making architectural decisions
- Modifying CI/CD configuration
- Any security-sensitive changes

## Testing

- All new features must include tests
- Bug fixes must include a regression test
- Run the full test suite before pushing
