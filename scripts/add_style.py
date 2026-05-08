#!/usr/bin/env python3
"""Add a style card directory and append it to registry.yml."""

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
    return "-".join("".join(out).split("-")) or "new-style"


def insert_before_toolchains(block: str) -> None:
    text = REGISTRY.read_text(encoding="utf-8")
    marker = "\ntoolchains:\n"
    if marker in text:
        text = text.replace(marker, "\n" + block.rstrip() + "\n" + marker, 1)
    else:
        text = text.rstrip() + "\n" + block.rstrip() + "\n"
    REGISTRY.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--style-card", required=True)
    parser.add_argument("--slide-map")
    parser.add_argument("--contact-sheet")
    parser.add_argument("--use-when", default="自定义 PPT 风格")
    args = parser.parse_args()

    name = slugify(args.name)
    target_dir = ROOT / "references" / "styles" / name
    target_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(args.style_card, target_dir / "style-card.md")
    if args.slide_map:
        shutil.copyfile(args.slide_map, target_dir / "slide-type-map.md")
    else:
        (target_dir / "slide-type-map.md").write_text(
            "# Slide Type Map\n\n- 根据内容类型选择最接近的模板页型。\n",
            encoding="utf-8",
        )
    asset_lines = ""
    if args.contact_sheet:
        shutil.copyfile(args.contact_sheet, target_dir / "contact-sheet.png")
        asset_lines = f"\n    assets:\n      contact_sheet: references/styles/{name}/contact-sheet.png"

    block = f"""  {name}:
    path: references/styles/{name}/style-card.md
    slide_map: references/styles/{name}/slide-type-map.md{asset_lines}
    use_when: {args.use_when}
"""
    insert_before_toolchains(block)
    print(f"added style: {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
