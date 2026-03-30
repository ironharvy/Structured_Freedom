# Windsurf Instructions

Read `AGENTS.md` first for shared conventions.

## Role

You are a collaborator on Structured Freedom, an AI-based MUD generator. Multiple AI agents work on this repo. Follow the coordination rules in AGENTS.md strictly.

## Workflow

- Always create a feature branch with the `windsurf/` prefix
- Check open PRs and recent commits before starting work to avoid conflicts
- Write tests for all new code
- Keep PRs small and focused

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
