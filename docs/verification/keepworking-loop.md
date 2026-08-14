# Verification — Keep Working Loop v0.1.0

## Release contract

- Public distribution is an independently authored, generalized override.
- The original source skill is read-only; its hash is recorded by the importer.
- The public package contains no personal path, client identifier, credential, or private runtime dependency.
- The behavior fixture requires goal locking, a verifier, a failure signature, minimal repair, re-verification, and explicit remaining risk.

## Required evidence before release promotion

1. `CLAUDE_SKILLS_HOME=<source> python tools/import_and_analyze.py`
2. `python tools/validate_repo.py`
3. Python compilation and `git diff --check`
4. A fresh Claude Code session smoke using `tests/fixtures/keepworking-conversation.md`
5. A fresh clone repeats importer and validator successfully
6. Remote branch, release metadata, and installed package are read back

## Current status

- Static repository validation: passed on 2026-08-11; importer, validator, Python compilation, and diff whitespace check completed before this record is updated.
- Fresh Claude Code behavior smoke: pending
- Fresh clone validation: pending
- Public release promotion: pending

Do not describe this skill as behavior-verified or release-verified until the fresh-session smoke and fresh-clone records are attached.
