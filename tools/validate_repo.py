#!/usr/bin/env python3
"""Validate standalone Claude Code skills before plugin bundling."""
from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []
TEXT_EXTENSIONS = {".md", ".json", ".py", ".txt", ".yml", ".yaml", ".toml"}
FORBIDDEN = {
    "private Windows path": re.compile(r"(?i)(?<!\$\{)[A-Z]:[\\/](?:Users|workspace|내 드라이브|Obsidian)"),
    "private Unix path": re.compile(r"(?i)(?:/Users/[^<\s`]+|/home/[^<\s`]+|/mnt/(?:skills|user-data)/[^<\s`]*)"),
    "personal identifier": re.compile(r"(?:신재현|재현님|C:[\\/]Users[\\/]jaehy|/Users/jaehy|/home/jaehy)"),
    "internal runtime coupling": re.compile(r"(?i)\b(?:Hermes|OpenClaw|muse|Sonatine|Cassandra|Anais|mary-jane)\b"),
    "client identifier": re.compile(r"(?:HF_|KHPT|비대면채널|주택연금)"),
    "credential assignment": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"][^'\"]{8,}"),
}
REQUIRED_SKILL_SECTIONS = [
    "## 언제 사용하면 좋은가",
    "## 사용하지 않는 경우",
    "## 입력",
    "## 산출물",
    "## 워크플로우",
    "## 실패와 복구",
    "## Anti-rationalization",
]


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


def validate_selection() -> tuple[list[str], dict]:
    config = load_json(ROOT / "config" / "selection.json")
    selected = list(config.get("skills", []))
    limit = config.get("daily_release_limit")
    if not isinstance(limit, int) or limit not in {1, 2}:
        error("daily_release_limit must be 1 or 2")
    if len(selected) > (limit or 0):
        error("selected skills exceed daily release limit")
    if len(selected) != len(set(selected)):
        error("duplicate selected skill")
    if config.get("plugins"):
        error("plugin bundling is deferred until standalone skill validation")
    return selected, config


def validate_skills(selected: list[str]) -> None:
    skills_root = ROOT / "skills"
    actual = sorted(p.name for p in skills_root.iterdir() if p.is_dir()) if skills_root.is_dir() else []
    if actual != sorted(selected):
        error(f"standalone skill set mismatch: expected={sorted(selected)} actual={actual}")
    for name in selected:
        path = skills_root / name / "SKILL.md"
        if not path.is_file():
            error(f"missing SKILL.md: skills/{name}")
            continue
        frontmatter = parse_frontmatter(path)
        if frontmatter.get("name") != name:
            error(f"skill name mismatch: skills/{name}")
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_SKILL_SECTIONS:
            if section not in text:
                error(f"missing required section {section}: skills/{name}/SKILL.md")
        trigger_count = len(re.findall(r"^- `[^`]+`$", text, re.MULTILINE))
        if trigger_count < 5:
            error(f"fewer than five trigger examples: skills/{name}/SKILL.md")
        if not (skills_root / name / "README.md").is_file():
            error(f"missing usage guide: skills/{name}/README.md")


def validate_manifest(selected: list[str]) -> None:
    manifest = load_json(ROOT / "docs" / "analysis" / "source-manifest.json")
    manifested = {row.get("skill") for row in manifest.get("files", [])}
    if set(selected) - manifested:
        error(f"selected skills missing from source manifest: {sorted(set(selected) - manifested)}")
    for row in manifest.get("files", []):
        if row.get("relative_path") == "SKILL.md" and not row.get("source_sha256"):
            error(f"missing source hash for imported SKILL.md: {row.get('skill')}")


def validate_fixture(selected: list[str]) -> None:
    for name in selected:
        fixture = ROOT / "tests" / "fixtures" / f"{name}-conversation.md"
        contract = ROOT / "tests" / "expected" / f"{name}-contract.json"
        if not fixture.is_file() or not contract.is_file():
            error(f"missing behavior fixture/contract for {name}")
            continue
        data = load_json(contract)
        if data.get("skill") != name:
            error(f"fixture contract skill mismatch: {name}")
        if not data.get("required_output_markers"):
            error(f"fixture contract has no required markers: {name}")


def validate_content() -> None:
    roots = [ROOT / "skills", ROOT / "overrides", ROOT / "tests", ROOT / "docs", ROOT / "config"]
    paths = [
        path
        for base in roots
        if base.exists()
        for path in base.rglob("*")
        if path.is_file()
    ]
    paths.extend(
        path for path in [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CHANGELOG.md", ROOT / "CONTRIBUTING.md", ROOT / "SECURITY.md"]
        if path.is_file()
    )
    for path in sorted(set(paths)):
        if path.stat().st_size > 5 * 1024 * 1024:
            error(f"file exceeds 5 MiB: {path.relative_to(ROOT)}")
        if path.suffix.lower() in TEXT_EXTENSIONS:
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


def main() -> int:
    selected, _ = validate_selection()
    validate_skills(selected)
    validate_manifest(selected)
    validate_fixture(selected)
    validate_content()
    print(json.dumps({
        "status": "PASS" if not ERRORS else "FAIL",
        "errors": ERRORS,
        "warnings": WARNINGS,
        "release_mode": "standalone-skill-first",
        "plugins": 0,
        "skills": len(selected),
    }, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
