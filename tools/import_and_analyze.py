#!/usr/bin/env python3
"""Read-only Claude skill analyzer and sanitized importer.

The source tree is never mutated. Selected skills are copied into this repository,
portable placeholders are applied, and source/destination hashes are recorded.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "selection.json"
ANALYSIS_DIR = REPO_ROOT / "docs" / "analysis"
OVERRIDES_ROOT = REPO_ROOT / "overrides"

TEXT_EXTENSIONS = {".md", ".json", ".py", ".txt", ".yaml", ".yml", ".toml"}

LITERAL_REPLACEMENTS = {
    "C:\\Users\\jaehy": "${USER_HOME}",
    "C:/Users/jaehy": "${USER_HOME}",
    "D:\\workspace": "${WORKSPACE_ROOT}",
    "D:/workspace": "${WORKSPACE_ROOT}",
    "F:\\Obsidian\\Jaehyun": "${KNOWLEDGE_ROOT}",
    "F:/Obsidian/Jaehyun": "${KNOWLEDGE_ROOT}",
    "신재현": "사용자",
    "재현님": "사용자",
    "/mnt/skills/public-portal-benchmark/": "",
    "/mnt/skills/asis-tobe-analysis/": "",
    "/mnt/skills/wireframe-composer/": "",
}

RISK_PATTERNS = {
    "absolute_windows_path": re.compile(r"(?i)(?<![A-Z0-9_])[A-Z]:[\\/][^\s`'\"<>]+"),
    "private_unix_path": re.compile(r"(?i)(?:/Users/|/home/|/mnt/)[^\s`'\"<>]+"),
    "credential_language": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|client[_ -]?secret|password|cookie|oauth)\b"),
    "runtime_coupling": re.compile(r"(?i)\b(?:Gemini|Hermes|Codex|OpenClaw|muse)\b"),
    "external_action": re.compile(r"(?i)\b(?:send|upload|publish|delete|move|rename|comment|email)\b"),
    "client_identifier": re.compile(r"(?:HF_|KHPT|비대면채널|주택연금)"),
    "personal_identifier": re.compile(r"(?:신재현|재현님|jaehy)"),
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
    # Generalize any remaining drive-rooted user/project examples without
    # retaining the original private path in the distribution copy.
    general_rules = [
        (re.compile(r"(?i)[A-Z]:[\\/]Users[\\/][^\\/\s`'\"<>]+"), "${USER_HOME}"),
        (re.compile(r"(?i)[A-Z]:[\\/]workspace"), "${WORKSPACE_ROOT}"),
    ]
    for pattern, replacement in general_rules:
        text, count = pattern.subn(replacement, text)
        if count:
            applied.append(f"regex:{pattern.pattern}:{count}")
    return text, sorted(set(applied))


def risk_flags(text: str) -> dict[str, int]:
    return {name: len(pattern.findall(text)) for name, pattern in RISK_PATTERNS.items()}


def inventory(source_root: Path) -> tuple[list[dict], list[dict]]:
    skill_dirs = sorted(p.parent for p in source_root.glob("*/SKILL.md"))
    names = {p.name for p in skill_dirs}
    rows: list[dict] = []
    edges: list[dict] = []
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        text = read_text(skill_file)
        referenced = sorted(
            other for other in names
            if other != skill_dir.name and re.search(rf"(?<![\w-]){re.escape(other)}(?![\w-])", text)
        )
        for target in referenced:
            edges.append({"source": skill_dir.name, "target": target})
        files = [p for p in skill_dir.rglob("*") if p.is_file()]
        aggregate = "\n".join(read_text(p) for p in files if p.suffix.lower() in TEXT_EXTENSIONS)
        rows.append({
            "name": skill_dir.name,
            "file_count": len(files),
            "references": referenced,
            "risk_flags": risk_flags(aggregate),
            "skill_sha256": sha256_bytes(skill_file.read_bytes()),
        })
    return rows, edges


def import_selected(source_root: Path, config: dict) -> list[dict]:
    source_root = source_root.resolve()
    if not source_root.exists():
        raise SystemExit(f"Claude skills source not found: {source_root}")
    if REPO_ROOT.resolve().is_relative_to(source_root):
        raise SystemExit("Destination must not be inside the Claude source tree")

    manifest: list[dict] = []
    for plugin_name, skill_names in config["plugins"].items():
        plugin_skills = REPO_ROOT / "plugins" / plugin_name / "skills"
        plugin_skills.mkdir(parents=True, exist_ok=True)
        selected_set = set(skill_names)
        for stale in plugin_skills.iterdir():
            if stale.is_dir() and stale.name not in selected_set:
                shutil.rmtree(stale)
        for skill_name in skill_names:
            source_dir = (source_root / skill_name).resolve()
            if source_dir.parent != source_root or not (source_dir / "SKILL.md").is_file():
                raise SystemExit(f"Invalid or missing selected skill: {skill_name}")
            override_dir = OVERRIDES_ROOT / plugin_name / skill_name
            destination_dir = plugin_skills / skill_name
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
                transformations: list[str] = []
                override_file = override_dir / relative
                if override_file.is_file():
                    destination_file.write_bytes(override_file.read_bytes())
                    transformations = ["maintainer_override"]
                elif source_file.suffix.lower() in TEXT_EXTENSIONS:
                    text = source_bytes.decode("utf-8", errors="replace")
                    sanitized, transformations = sanitize_text(text)
                    destination_file.write_text(sanitized, encoding="utf-8", newline="\n")
                else:
                    destination_file.write_bytes(source_bytes)
                destination_bytes = destination_file.read_bytes()
                manifest.append({
                    "plugin": plugin_name,
                    "skill": skill_name,
                    "relative_path": relative.as_posix(),
                    "source_sha256": before_hashes[source_file],
                    "distribution_sha256": sha256_bytes(destination_bytes),
                    "transformations": transformations,
                    "distribution_risk_flags": risk_flags(
                        destination_bytes.decode("utf-8", errors="replace")
                        if destination_file.suffix.lower() in TEXT_EXTENSIONS else ""
                    ),
                })
            if override_dir.is_dir():
                for override_file in sorted(p for p in override_dir.rglob("*") if p.is_file()):
                    relative = override_file.relative_to(override_dir)
                    if relative in copied_relatives:
                        continue
                    destination_file = destination_dir / relative
                    destination_file.parent.mkdir(parents=True, exist_ok=True)
                    destination_bytes = override_file.read_bytes()
                    destination_file.write_bytes(destination_bytes)
                    manifest.append({
                        "plugin": plugin_name,
                        "skill": skill_name,
                        "relative_path": relative.as_posix(),
                        "source_sha256": None,
                        "distribution_sha256": sha256_bytes(destination_bytes),
                        "transformations": ["maintainer_added"],
                        "distribution_risk_flags": risk_flags(
                            destination_bytes.decode("utf-8", errors="replace")
                            if destination_file.suffix.lower() in TEXT_EXTENSIONS else ""
                        ),
                    })
            # Re-read every source file and assert source immutability.
            for source_file, expected_hash in before_hashes.items():
                actual_hash = sha256_bytes(source_file.read_bytes())
                if actual_hash != expected_hash:
                    raise SystemExit(f"SOURCE MUTATION DETECTED: {source_file}")
    return manifest


def write_reports(rows: list[dict], edges: list[dict], manifest: list[dict], config: dict) -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    (ANALYSIS_DIR / "full-inventory.json").write_text(
        json.dumps({"count": len(rows), "skills": rows, "edges": edges}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (ANALYSIS_DIR / "source-manifest.json").write_text(
        json.dumps({"schema_version": "1.0.0", "files": manifest}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    selected = {name for names in config["plugins"].values() for name in names}
    selected_rows = [row for row in rows if row["name"] in selected]
    flag_totals = Counter()
    for row in selected_rows:
        flag_totals.update(row["risk_flags"])
    lines = [
        "# Claude Source Skill Analysis",
        "",
        f"- Direct top-level skills discovered: **{len(rows)}**",
        f"- Selected distribution candidates: **{len(selected_rows)}**",
        f"- Cross-skill references discovered: **{len(edges)}**",
        "- Source mutation check: **PASS**",
        "",
        "## Selected workflow boundaries",
        "",
    ]
    for plugin, names in config["plugins"].items():
        lines.append(f"### `{plugin}`")
        lines.extend(f"- `{name}`" for name in names)
        lines.append("")
    lines.extend(["## Portability flags before manual review", ""])
    for key, value in sorted(flag_totals.items()):
        lines.append(f"- `{key}`: {value}")
    lines.extend([
        "",
        "> Flags are review signals, not confirmed secrets. Publication remains blocked until the sanitized copies pass the repository validator.",
        "",
    ])
    (ANALYSIS_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    default_root = Path(config["default_source_root"]).expanduser()
    source_root = Path(os.environ.get(config["source_root_env"], default_root)).expanduser()
    rows, edges = inventory(source_root)
    manifest = import_selected(source_root, config)
    write_reports(rows, edges, manifest, config)
    print(json.dumps({
        "source_root": str(source_root),
        "direct_skill_count": len(rows),
        "selected_skill_count": sum(len(v) for v in config["plugins"].values()),
        "copied_file_count": len(manifest),
        "source_immutability": "PASS",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
