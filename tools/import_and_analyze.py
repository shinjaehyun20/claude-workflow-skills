#!/usr/bin/env python3
"""Read-only Claude skill analyzer and standalone skill importer.

Selected source skills are copied into this repository, reviewed overrides are
applied, and source/distribution hashes are recorded. Source-runtime files are
never mutated.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "selection.json"
ANALYSIS_DIR = REPO_ROOT / "docs" / "analysis"
OVERRIDES_ROOT = REPO_ROOT / "overrides"
SKILLS_ROOT = REPO_ROOT / "skills"
TEXT_EXTENSIONS = {".md", ".json", ".py", ".txt", ".yaml", ".yml", ".toml"}
ALLOWED_AUTHORSHIP = {"owner-authored"}
REQUIRED_GENERALIZATION = "generalized"

LITERAL_REPLACEMENTS = {
    "C:\\Users\\jaehy": "${USER_HOME}",
    "C:/Users/jaehy": "${USER_HOME}",
    "D:\\workspace": "${WORKSPACE_ROOT}",
    "D:/workspace": "${WORKSPACE_ROOT}",
    "F:\\Obsidian\\Jaehyun": "${KNOWLEDGE_ROOT}",
    "F:/Obsidian/Jaehyun": "${KNOWLEDGE_ROOT}",
    "신재현": "사용자",
    "재현님": "사용자",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def sanitize_text(text: str) -> tuple[str, list[str]]:
    applied: list[str] = []
    for old, new in LITERAL_REPLACEMENTS.items():
        if old in text:
            text = text.replace(old, new)
            applied.append(f"literal:{old[:24]}")
    rules = [
        (re.compile(r"(?i)[A-Z]:[\\/]Users[\\/][^\\/\s`'\"<>]+"), "${USER_HOME}"),
        (re.compile(r"(?i)[A-Z]:[\\/]workspace"), "${WORKSPACE_ROOT}"),
    ]
    for pattern, replacement in rules:
        text, count = pattern.subn(replacement, text)
        if count:
            applied.append(f"regex:{pattern.pattern}:{count}")
    return text, sorted(set(applied))


def validate_release_eligibility(config: dict, selected: list[str]) -> dict:
    """Fail closed unless every selected skill is owner-authored and generalized."""
    registry_relative = config.get("skill_registry")
    if not isinstance(registry_relative, str) or not registry_relative:
        raise SystemExit("skill_registry is required")
    registry_path = (REPO_ROOT / registry_relative).resolve()
    if not registry_path.is_relative_to(REPO_ROOT.resolve()) or not registry_path.is_file():
        raise SystemExit("Invalid or missing skill registry")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    records = registry.get("skills", {})
    for skill_name in selected:
        record = records.get(skill_name)
        if not isinstance(record, dict):
            raise SystemExit(f"Selected skill is not registered: {skill_name}")
        if record.get("authorship") not in ALLOWED_AUTHORSHIP:
            raise SystemExit(f"Selected skill is not owner-authored: {skill_name}")
        if record.get("generalization") != REQUIRED_GENERALIZATION:
            raise SystemExit(f"Selected skill is not generalized: {skill_name}")
        if record.get("publication_eligible") is not True:
            raise SystemExit(f"Selected skill is not publication eligible: {skill_name}")
    return registry


def inventory_summary(source_root: Path, selected: list[str]) -> dict:
    skill_dirs = sorted(p.parent for p in source_root.glob("*/SKILL.md"))
    names = {p.name for p in skill_dirs}
    return {
        "schema_version": "2.0.0",
        "direct_top_level_skill_count": len(skill_dirs),
        "selected_skill_count": len(selected),
        "selected_skills": selected,
        "missing_selected_skills": sorted(set(selected) - names),
    }


def import_selected(source_root: Path, selected: list[str]) -> list[dict]:
    source_root = source_root.resolve()
    if not source_root.exists():
        raise SystemExit(f"Claude skills source not found: {source_root}")
    if REPO_ROOT.resolve().is_relative_to(source_root):
        raise SystemExit("Destination must not be inside the Claude source tree")

    SKILLS_ROOT.mkdir(parents=True, exist_ok=True)
    selected_set = set(selected)
    for stale in SKILLS_ROOT.iterdir():
        if stale.is_dir() and stale.name not in selected_set:
            shutil.rmtree(stale)

    manifest: list[dict] = []
    for skill_name in selected:
        source_dir = (source_root / skill_name).resolve()
        if source_dir.parent != source_root or not (source_dir / "SKILL.md").is_file():
            raise SystemExit(f"Invalid or missing selected skill: {skill_name}")
        override_dir = OVERRIDES_ROOT / skill_name
        destination_dir = SKILLS_ROOT / skill_name
        if destination_dir.exists():
            shutil.rmtree(destination_dir)
        destination_dir.mkdir(parents=True)

        before_hashes: dict[Path, str] = {}
        copied_relatives: set[Path] = set()
        for source_file in sorted(p for p in source_dir.rglob("*") if p.is_file()):
            relative = source_file.relative_to(source_dir)
            copied_relatives.add(relative)
            source_bytes = source_file.read_bytes()
            before_hashes[source_file] = sha256_bytes(source_bytes)
            destination_file = destination_dir / relative
            destination_file.parent.mkdir(parents=True, exist_ok=True)
            override_file = override_dir / relative
            if override_file.is_file():
                if override_file.suffix.lower() in TEXT_EXTENSIONS:
                    destination_file.write_text(read_text(override_file), encoding="utf-8", newline="\n")
                else:
                    destination_file.write_bytes(override_file.read_bytes())
                transformations = ["maintainer_override"]
            elif source_file.suffix.lower() in TEXT_EXTENSIONS:
                sanitized, transformations = sanitize_text(
                    source_bytes.decode("utf-8", errors="replace")
                )
                destination_file.write_text(sanitized, encoding="utf-8", newline="\n")
            else:
                destination_file.write_bytes(source_bytes)
                transformations = []
            manifest.append({
                "skill": skill_name,
                "relative_path": relative.as_posix(),
                "source_sha256": before_hashes[source_file],
                "distribution_sha256": sha256_bytes(destination_file.read_bytes()),
                "transformations": transformations,
            })

        if override_dir.is_dir():
            for override_file in sorted(p for p in override_dir.rglob("*") if p.is_file()):
                relative = override_file.relative_to(override_dir)
                if relative in copied_relatives:
                    continue
                destination_file = destination_dir / relative
                destination_file.parent.mkdir(parents=True, exist_ok=True)
                if override_file.suffix.lower() in TEXT_EXTENSIONS:
                    destination_file.write_text(read_text(override_file), encoding="utf-8", newline="\n")
                else:
                    destination_file.write_bytes(override_file.read_bytes())
                manifest.append({
                    "skill": skill_name,
                    "relative_path": relative.as_posix(),
                    "source_sha256": None,
                    "distribution_sha256": sha256_bytes(destination_file.read_bytes()),
                    "transformations": ["maintainer_added"],
                })

        for source_file, expected_hash in before_hashes.items():
            if sha256_bytes(source_file.read_bytes()) != expected_hash:
                raise SystemExit(f"SOURCE MUTATION DETECTED: {source_file}")
    return manifest


def write_reports(summary: dict, manifest: list[dict]) -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    (ANALYSIS_DIR / "inventory-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    (ANALYSIS_DIR / "source-manifest.json").write_text(
        json.dumps({"schema_version": "2.0.0", "files": manifest}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    lines = [
        "# Claude Source Skill Analysis",
        "",
        f"- Direct top-level skills discovered: **{summary['direct_top_level_skill_count']}**",
        f"- Selected standalone skills: **{summary['selected_skill_count']}**",
        f"- Current release: `{', '.join(summary['selected_skills'])}`",
        "- Source mutation check: **PASS**",
        "- Full private inventory is intentionally not published.",
        "",
    ]
    (ANALYSIS_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    selected = list(config.get("skills", []))
    if len(selected) > int(config.get("daily_release_limit", 2)):
        raise SystemExit("Selected skill count exceeds daily release limit")
    validate_release_eligibility(config, selected)
    source_root = Path(
        os.environ.get(config["source_root_env"], Path(config["default_source_root"]).expanduser())
    ).expanduser()
    summary = inventory_summary(source_root, selected)
    if summary["missing_selected_skills"]:
        raise SystemExit(f"Missing selected skills: {summary['missing_selected_skills']}")
    manifest = import_selected(source_root, selected)
    write_reports(summary, manifest)
    print(json.dumps({
        "source_root": str(source_root),
        "direct_skill_count": summary["direct_top_level_skill_count"],
        "selected_skill_count": len(selected),
        "copied_file_count": len(manifest),
        "source_immutability": "PASS",
        "release_mode": "standalone-skill-first",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
