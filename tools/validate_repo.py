#!/usr/bin/env python3
"""Validate the portable Claude Code marketplace repository."""
from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []

FORBIDDEN = {
    "private Windows path": re.compile(r"(?i)(?<!\$\{)[A-Z]:[\\/](?:Users|workspace|내 드라이브|Obsidian)"),
    "private Unix path": re.compile(r"(?i)(?:/Users/[^<\s`]+|/home/[^<\s`]+|/mnt/(?:skills|user-data)/[^<\s`]*)"),
    "personal identifier": re.compile(r"(?:신재현|재현님|C:[\\/]Users[\\/]jaehy|/Users/jaehy|/home/jaehy)"),
    "internal runtime coupling": re.compile(r"(?i)\b(?:Hermes|OpenClaw|muse|Sonatine|Cassandra|Anais|mary-jane)\b"),
    "client identifier": re.compile(r"(?:HF_|KHPT|비대면채널|주택연금)"),
    "credential assignment": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"][^'\"]{8,}"),
}


def error(message: str) -> None:
    ERRORS.append(message)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        error(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")
        return {}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        error(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        error(f"unterminated YAML frontmatter: {path.relative_to(ROOT)}")
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def validate_marketplace() -> None:
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    names: set[str] = set()
    for entry in marketplace.get("plugins", []):
        name = entry.get("name")
        if not name or name in names:
            error(f"missing or duplicate marketplace plugin name: {name}")
            continue
        names.add(name)
        source = ROOT / str(entry.get("source", ""))
        manifest = load_json(source / ".claude-plugin" / "plugin.json")
        if manifest.get("name") != name:
            error(f"plugin name mismatch: {name}")
        skills_dir = source / "skills"
        if not skills_dir.is_dir():
            error(f"missing skills directory: {skills_dir.relative_to(ROOT)}")
            continue
        for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.is_file():
                error(f"missing SKILL.md: {skill_dir.relative_to(ROOT)}")
                continue
            frontmatter = parse_frontmatter(skill_file)
            if frontmatter.get("name") != skill_dir.name:
                error(f"skill name mismatch: {skill_dir.relative_to(ROOT)}")


def validate_content() -> None:
    roots = [ROOT / "plugins", ROOT / "overrides"]
    for base in roots:
        for path in sorted(p for p in base.rglob("*") if p.is_file()):
            if path.stat().st_size > 5 * 1024 * 1024:
                error(f"file exceeds 5 MiB: {path.relative_to(ROOT)}")
            if path.suffix.lower() in {".md", ".json", ".py", ".txt", ".yml", ".yaml", ".toml"}:
                text = path.read_text(encoding="utf-8", errors="replace")
                for label, pattern in FORBIDDEN.items():
                    if pattern.search(text):
                        error(f"{label}: {path.relative_to(ROOT)}")
            if path.suffix.lower() == ".json":
                load_json(path)
            if path.suffix.lower() == ".py":
                try:
                    py_compile.compile(str(path), doraise=True)
                except Exception as exc:
                    error(f"Python syntax: {path.relative_to(ROOT)}: {exc}")
            if path.is_symlink():
                error(f"symlink not allowed: {path.relative_to(ROOT)}")


def validate_selection() -> None:
    selection = load_json(ROOT / "config" / "selection.json")
    manifest = load_json(ROOT / "docs" / "analysis" / "source-manifest.json")
    selected = {(plugin, skill) for plugin, skills in selection.get("plugins", {}).items() for skill in skills}
    manifested = {(row.get("plugin"), row.get("skill")) for row in manifest.get("files", [])}
    missing = selected - manifested
    if missing:
        error(f"selected skills missing from source manifest: {sorted(missing)}")
    for plugin, skill in selected:
        if not (ROOT / "plugins" / plugin / "skills" / skill / "SKILL.md").is_file():
            error(f"selected distribution skill missing: {plugin}/{skill}")


def main() -> int:
    validate_marketplace()
    validate_content()
    validate_selection()
    print(json.dumps({
        "status": "PASS" if not ERRORS else "FAIL",
        "errors": ERRORS,
        "warnings": WARNINGS,
        "plugins": 3,
        "skills": sum(1 for _ in (ROOT / "plugins").glob("*/skills/*/SKILL.md")),
    }, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
