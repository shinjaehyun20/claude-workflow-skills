# Source Protection Contract

This repository is a sanitized distribution surface for Claude Code workflow skills.

## Immutable sources

- Claude Code source skills: `${CLAUDE_SKILLS_HOME}` (default: `~/.claude/skills`)
- Hermes skills and Codex skills may be inspected for publication patterns only.
- Never edit, delete, rename, move, or overwrite source-runtime files.
- All changes belong inside this repository.

## Lifecycle

`inventory -> select -> copy -> sanitize -> validate -> commit -> push -> remote verify`

## Publication gates

- A source hash must exist for every imported file.
- Absolute paths, personal names, client identifiers, tokens, cookies, OAuth state, and runtime-specific private configuration block publication.
- A plugin must pass `claude plugin validate`.
- Markdown links, JSON, Python syntax, and secret scanning must pass.
- Public visibility is a separate approval gate. Start private.
