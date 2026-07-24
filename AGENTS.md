# Source Protection Contract

This repository is a sanitized distribution surface for Claude Code workflow skills.

## Immutable sources

- Claude Code source skills: `${CLAUDE_SKILLS_HOME}` (default: `~/.claude/skills`)
- Non-target runtime skills may be inspected for publication patterns only.
- Never edit, delete, rename, move, or overwrite source-runtime files.
- All changes belong inside this repository.

## Lifecycle

`inventory -> select release batch 1~2 -> copy -> sanitize -> document -> accumulate in catalog -> static validate -> Claude smoke -> commit -> push -> remote verify`

## Standalone-first rule

- Release only skills confirmed as directly owner-authored in `config/skill-registry.json`.
- Third-party, adapted, forked, and unknown-authorship skills are not release candidates.
- A selected skill must be generalized before import; installation in the source directory is not authorship proof.
- Publish and validate each skill independently before plugin bundling.
- Every skill needs a usage guide, fixture, expected behavior contract, and actual Claude Code smoke record.
- Plugin manifest validation proves packaging only; it does not prove skill behavior.
- Add plugins only after related standalone skills have passed their own gates.
- `config/selection.json` is the current release batch; `config/skill-registry.json` and `skills/` are the cumulative published catalog. A new batch must not delete prior published skills.

## Publication gates

- A source hash must exist for every imported source file.
- Absolute paths, personal names, client identifiers, tokens, cookies, OAuth state, and runtime-specific private configuration block publication.
- Markdown links, JSON, Python syntax, risk scanning, and fixture contracts must pass.
- If plugins exist, each plugin must additionally pass `claude plugin validate` and install/update/remove smoke.
- Public visibility is a separate approval gate. Start private.
