#!/usr/bin/env python3
"""Add an audience card and append it to registry.yml."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.yml"


def slugify(value: str) -> str:
    out = []
    for ch in value.lower().strip():
        if ch.isalnum():
            out.append(ch)
        elif ch in {" ", "_", "-", "."}:
            out.append("-")
    return "-".join("".join(out).split("-")) or "new-audience"


def insert_before_reviewers(block: str) -> None:
    text = REGISTRY.read_text(encoding="utf-8")
    marker = "\nreviewers:\n"
    if marker in text:
        text = text.replace(marker, "\n" + block.rstrip() + "\n" + marker, 1)
    else:
        text = text.rstrip() + "\n" + block.rstrip() + "\n"
    REGISTRY.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--card", required=True)
    parser.add_argument("--use-when", default="自定义受众画像")
    args = parser.parse_args()

    name = slugify(args.name)
    target_dir = ROOT / "references" / "audiences" / name
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.card, target_dir / "audience-card.md")

    block = f"""  {name}:
    path: references/audiences/{name}/audience-card.md
    use_when: {args.use_when}
"""
    insert_before_reviewers(block)
    print(f"added audience: {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
