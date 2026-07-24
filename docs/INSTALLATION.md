# Installation

## Requirements

- Claude Code with plugin marketplace support
- Git
- Python 3.9+ only for folder-organizer scripts and maintainer validation

## GitHub marketplace

```text
/plugin marketplace add shinjaehyun20/wylie-claude-workflow-skills
```

Install only what the user needs:

```text
/plugin install wylie-document-quality@wylie-claude-workflow-skills
/plugin install wylie-ux-planning@wylie-claude-workflow-skills
/plugin install wylie-project-ops@wylie-claude-workflow-skills
```

Restart or reload Claude Code if newly installed skills are not discovered.

## Local review before remote publication

Clone or open the repository locally, then add its path as a marketplace source using the Claude Code plugin command supported by the installed version. Run:

```bash
python tools/validate_repo.py
```

## Verify

1. Confirm the marketplace appears in `/plugin`.
2. Confirm installed plugin name and version.
3. Ask Claude Code to list the plugin's skills.
4. Run one low-risk dry-run, such as source scan or folder organizer without `--apply`.
5. Check that no source file or external system was changed.

## Remove

Use Claude Code `/plugin` management to uninstall individual plugins and remove the marketplace source. Removing the plugin does not delete project outputs previously created by a skill.
