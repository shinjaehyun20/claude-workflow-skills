# Verification — Evidence-Backed Weekly Report v0.1.0

## Release contract

- The public distribution is an owner-authored, generalized rewrite of a private workflow pattern.
- The source workflow remains read-only; importer records source and distribution hashes.
- The public package contains no customer name, personal path, private runtime dependency, credential, or organization-specific submission endpoint.
- The fixture requires source coverage, complete prior-plan reconciliation, evidence-based attribution, and an explicit distinction between a local draft and external publication.

## Required evidence before release promotion

1. `python tools/import_and_analyze.py`
2. `python tools/validate_repo.py`
3. `python -m py_compile tools/import_and_analyze.py tools/validate_repo.py`
4. `git diff --check`
5. A fresh Claude Code session smoke using `tests/fixtures/weekly-report-evidence-conversation.md`
6. A fresh clone repeats importer and validator successfully
7. Remote branch, release metadata, and installed package are read back

## Current status

- Static repository validation: passed on 2026-08-14.
- Fresh Claude Code behavior smoke: passed on 2026-08-14 with the fixture scenario. The response locked the reporting period, created source coverage, reconciled all three prior-plan items, kept the migration in progress, excluded the automated-only item from personal-performance claims, and performed no send or publish action. Expected markers: 6/6; forbidden markers: 0.
- Fresh clone validation: pending push.
- Public release promotion: pending push and remote read-back.

Static validation and behavior smoke are separate evidence. Do not describe this skill as release-verified until the pushed branch and fresh clone have been verified.
