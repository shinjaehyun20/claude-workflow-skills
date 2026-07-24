from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def build_summary(root: Path) -> dict:
    directories = []
    file_samples = []
    keyword_counter: Counter[str] = Counter()

    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_dir():
            directories.append(rel)
            continue
        file_samples.append(rel)
        stem = path.stem.replace("_", " ").replace("-", " ")
        for token in stem.split():
            cleaned = token.strip("()[]{}.,")
            if len(cleaned) >= 2:
                keyword_counter[cleaned] += 1

    return {
      "template_root": str(root),
      "top_level_directories": sorted(p.name for p in root.iterdir() if p.is_dir()),
      "directory_count": len(directories),
      "file_count": len(file_samples),
      "directories": directories,
      "file_samples": file_samples[:200],
      "common_tokens": keyword_counter.most_common(100),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a template directory and emit a compact JSON summary.")
    parser.add_argument("template_root", type=Path)
    parser.add_argument("--output", type=Path, help="Optional JSON file path.")
    args = parser.parse_args()

    root = args.template_root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Template root not found: {root}")

    summary = build_summary(root)
    text = json.dumps(summary, ensure_ascii=False, indent=2)

    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
