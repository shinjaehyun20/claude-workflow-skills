# Contributing

## Principles

- Do not edit source-runtime skill directories.
- Add a source skill to `config/selection.json`, then provide portable changes under `overrides/<plugin>/<skill>/`.
- Do not commit client data, personal paths, tokens, cookies, OAuth state, or internal messages.
- Keep skills usable without a particular OS, account, MCP server, or AI runtime unless the dependency is explicit and optional.

## Development

```bash
python tools/import_and_analyze.py
python tools/validate_repo.py
```

A contribution must include:

1. workflow position and target user
2. required and optional dependencies
3. input/output contract
4. safe fallback when a tool is unavailable
5. verification evidence
6. changelog entry

## Pull request gate

- Source immutability: PASS
- Repository validation: PASS
- Claude plugin validation: PASS
- Secret scan: PASS
- No unapproved client identifiers: PASS
- README/docs updated: PASS
