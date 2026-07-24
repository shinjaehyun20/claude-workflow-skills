# Source Protection Contract

This repository is a sanitized distribution surface for Claude Code workflow skills.

## Immutable sources

- Claude Code source skills: `${CLAUDE_SKILLS_HOME}` (default: `~/.claude/skills`)
- Non-target runtime skills may be inspected for publication patterns only.
- Never edit, delete, rename, move, or overwrite source-runtime files.
- All changes belong inside this repository.

## Lifecycle

`inventory -> select 1~2 -> copy -> sanitize -> document -> static validate -> Claude smoke -> commit -> push -> remote verify`

## Standalone-first rule

- Publish and validate each skill independently before plugin bundling.
- Every skill needs a usage guide, fixture, expected behavior contract, and actual Claude Code smoke record.
- Plugin manifest validation proves packaging only; it does not prove skill behavior.
- Add plugins only after related standalone skills have passed their own gates.

## Publication gates

- A source hash must exist for every imported source file.
- Absolute paths, personal names, client identifiers, tokens, cookies, OAuth state, and runtime-specific private configuration block publication.
- Markdown links, JSON, Python syntax, risk scanning, and fixture contracts must pass.
- If plugins exist, each plugin must additionally pass `claude plugin validate` and install/update/remove smoke.
- Public visibility is a separate approval gate. Start private.
