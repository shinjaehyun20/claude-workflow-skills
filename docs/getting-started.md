# Getting Started

This guide installs one skill into one project, runs a low-risk first use, and shows how to verify the local package.

## 1. Get the repository

```bash
git clone https://github.com/shinjaehyun20/claude-workflow-skills.git
cd claude-workflow-skills
```

## 2. Choose a skill

Start with `weekly-report-evidence` when a weekly report must reconcile a prior plan with current records.

```bash
SKILL_NAME=weekly-report-evidence
```

Read the package guide before installation:

```text
skills/weekly-report-evidence/README.md
```

## 3. Install into one project

From the target project root:

```bash
mkdir -p .claude/skills
cp -R "<repository>/skills/$SKILL_NAME" .claude/skills/
```

Project-local installation is the recommended default. If the same skill name already exists, compare it before replacing anything.

## 4. Try a low-risk request

Use a bounded reporting period and local source records. Do not ask the skill to send, publish, or overwrite files during the first check.

```text
/weekly-report-evidence Create a weekly report draft from the previous report and this week's work logs. Mark unsupported statements as confirmation needed. Do not send or publish anything.
```

## 5. Verify the package

Run the repository checks before distributing a modified package:

```bash
python tools/import_and_analyze.py
python tools/validate_repo.py
python -m py_compile tools/import_and_analyze.py tools/validate_repo.py
git diff --check
```

These checks validate package structure, registry consistency, source immutability, and public-safety patterns. They do not replace a fresh Claude Code behavior smoke.

## Next

- Browse the [skill catalog](../README.md#제공-스킬).
- Read [installation details](INSTALLATION.md).
- Use the [publication checklist](discovery-checklist.md) before creating a release.
