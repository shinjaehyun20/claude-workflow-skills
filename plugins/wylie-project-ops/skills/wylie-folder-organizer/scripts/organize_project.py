from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_RULES = SKILL_DIR / "references" / "routing-rules.json"


def normalize(value: str) -> str:
    value = value.casefold()
    return re.sub(r"[^0-9a-z가-힣]+", "", value)


@dataclass(frozen=True)
class Route:
    path: str
    any_tokens: tuple[str, ...]
    all_tokens: tuple[str, ...]

    @classmethod
    def from_dict(cls, item: dict) -> "Route":
        return cls(
            path=item["path"],
            any_tokens=tuple(normalize(token) for token in item.get("any", [])),
            all_tokens=tuple(normalize(token) for token in item.get("all", [])),
        )

    def matches(self, normalized_name: str) -> bool:
        if self.all_tokens and not all(token in normalized_name for token in self.all_tokens):
            return False
        if self.any_tokens and not any(token in normalized_name for token in self.any_tokens):
            return False
        return bool(self.all_tokens or self.any_tokens)


def load_rules(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["routes"] = [Route.from_dict(item) for item in data["routes"]]
    data["ignore_filenames"] = {normalize(name) for name in data.get("ignore_filenames", [])}
    return data


def iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def classify(file_path: Path, target_root: Path, routes: list[Route], ignore_names: set[str]) -> dict:
    rel_path = file_path.relative_to(target_root)
    normalized_name = normalize(file_path.stem)
    normalized_filename = normalize(file_path.name)

    if normalized_filename in ignore_names:
        return {"status": "ignored", "source": rel_path.as_posix(), "reason": "ignored filename"}

    for route in routes:
        if route.matches(normalized_name):
            destination_dir = Path(route.path)
            destination = destination_dir / file_path.name
            current_parent = rel_path.parent.as_posix()
            destination_parent = destination_dir.as_posix()
            if current_parent == destination_parent or current_parent.startswith(destination_parent + "/"):
                return {
                    "status": "already_in_place",
                    "source": rel_path.as_posix(),
                    "destination": destination.as_posix(),
                    "matched_path": route.path,
                }
            return {
                "status": "move",
                "source": rel_path.as_posix(),
                "destination": destination.as_posix(),
                "matched_path": route.path,
            }

    return {"status": "unmatched", "source": rel_path.as_posix()}


def choose_destination(path: Path) -> Path:
    if not path.exists():
        return path
    counter = 1
    while True:
        candidate = path.with_name(f"{path.stem}__dup{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def apply_move(target_root: Path, item: dict) -> dict:
    source = target_root / item["source"]
    destination = choose_destination(target_root / item["destination"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    source.rename(destination)
    item["destination"] = destination.relative_to(target_root).as_posix()
    item["status"] = "moved"
    return item


def main() -> int:
    parser = argparse.ArgumentParser(description="Organize a project directory using Wylie routing rules.")
    parser.add_argument("target_root", type=Path)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--apply", action="store_true", help="Actually move files.")
    parser.add_argument("--report", type=Path, help="Optional JSON report path.")
    parser.add_argument("--unmatched-to", type=str, help="Relative folder for unmatched files when --apply is used.")
    args = parser.parse_args()

    target_root = args.target_root.expanduser().resolve()
    rules_path = args.rules.expanduser().resolve()

    if not target_root.exists() or not target_root.is_dir():
        raise SystemExit(f"Target root not found: {target_root}")
    if not rules_path.exists():
        raise SystemExit(f"Rules file not found: {rules_path}")

    rules = load_rules(rules_path)
    report: list[dict] = []

    for file_path in iter_files(target_root):
        item = classify(file_path, target_root, rules["routes"], rules["ignore_filenames"])
        if item["status"] == "unmatched" and args.unmatched_to:
            item["destination"] = str(Path(args.unmatched_to) / Path(item["source"]).name).replace("\\", "/")
            item["matched_path"] = args.unmatched_to
            item["status"] = "move"
        report.append(item)

    if args.apply:
        for item in report:
            if item["status"] == "move":
                apply_move(target_root, item)

    summary = {
        "target_root": str(target_root),
        "rules_path": str(rules_path),
        "apply": args.apply,
        "counts": {},
        "items": report,
    }

    for key in ("ignored", "already_in_place", "move", "moved", "unmatched"):
        summary["counts"][key] = sum(1 for item in report if item["status"] == key)

    output = json.dumps(summary, ensure_ascii=False, indent=2)
    print(output)

    if args.report:
        args.report.write_text(output, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
