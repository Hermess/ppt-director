#!/usr/bin/env python3
"""Validate ppt-director registry path references without external deps."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.yml"


PATH_RE = re.compile(r"^\s+(?:path|slide_map):\s+(.+?)\s*$")
ASSET_RE = re.compile(r"^\s+contact_sheet:\s+(.+?)\s*$")


def main() -> int:
    if not REGISTRY.exists():
        print(f"FAIL missing registry: {REGISTRY}")
        return 1

    missing: list[Path] = []
    checked: list[Path] = []
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        match = PATH_RE.match(line) or ASSET_RE.match(line)
        if not match:
            continue
        rel = match.group(1).strip().strip('"').strip("'")
        target = ROOT / rel
        checked.append(target)
        if not target.exists():
            missing.append(target)

    if missing:
        print("FAIL missing registry targets:")
        for path in missing:
            print(f"- {path}")
        return 1

    print(f"PASS registry targets: {len(checked)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
