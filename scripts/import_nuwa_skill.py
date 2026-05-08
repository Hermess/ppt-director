#!/usr/bin/env python3
"""Convert a Nuwa-generated skill into a PPT Director card."""

from __future__ import annotations

import argparse
import re
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def slugify(value: str) -> str:
    out = []
    for ch in value.lower().strip():
        if ch.isalnum():
            out.append(ch)
        elif ch in {" ", "_", "-", "."}:
            out.append("-")
    return "-".join("".join(out).split("-")) or "nuwa-object"


def read_skill_md(source: Path) -> tuple[str, Path]:
    if source.is_file() and source.suffix == ".zip":
        tmp = Path(tempfile.mkdtemp(prefix="nuwa-skill-"))
        with zipfile.ZipFile(source) as archive:
            archive.extractall(tmp)
        candidates = list(tmp.rglob("SKILL.md"))
        if not candidates:
            raise FileNotFoundError("SKILL.md not found in zip")
        return candidates[0].read_text(encoding="utf-8"), tmp

    if source.is_dir():
        candidates = list(source.rglob("SKILL.md"))
        if not candidates:
            raise FileNotFoundError("SKILL.md not found in directory")
        return candidates[0].read_text(encoding="utf-8"), source

    raise FileNotFoundError(f"unsupported source: {source}")


def strip_frontmatter(text: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)


def section(text: str, title: str) -> str:
    pattern = rf"^##\s+.*{re.escape(title)}.*?\n(.*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text, flags=re.M | re.S)
    return match.group(1).strip() if match else ""


def bullets_from(text: str, limit: int = 8) -> list[str]:
    bullets = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- "):
            bullets.append(line[2:].strip())
        elif re.match(r"^\d+\.\s+", line):
            bullets.append(re.sub(r"^\d+\.\s+", "", line).strip())
        if len(bullets) >= limit:
            break
    return bullets


def card_for_reviewer(name: str, body: str) -> str:
    models = bullets_from(section(body, "核心心智模型"), 6)
    heuristics = bullets_from(section(body, "决策启发式"), 8)
    anti = bullets_from(section(body, "价值观与反模式"), 8)
    dna = bullets_from(section(body, "表达DNA"), 6)

    def list_or_default(items: list[str], default: str) -> str:
        values = items or [default]
        return "\n".join(f"- {item}" for item in values)

    return f"""# Reviewer Card: {name}

## Lens

由 Nuwa Skill 自动导入。用于从该对象的思维模型、决策启发式、表达 DNA 和反模式出发，审查 PPT 的逻辑、标题、内容取舍和风险。

## Cares About

{list_or_default(models + heuristics, "是否有清晰判断、结构抓手和可执行路径。")}

## Rejects

{list_or_default(anti, "空泛表达、逻辑跳跃、缺少证据和缺少受众价值。")}

## Expression Notes

{list_or_default(dna, "保持该对象的表达节奏，但不要进行未经要求的完整角色扮演。")}

## Review Checklist

- 每页标题是否有观点。
- 叙事链是否连贯。
- 是否遗漏该专家最关心的判断维度。
- 是否存在该专家会反感的空话、套话或证据不足。
- 是否需要新增、合并或删除页面。

## Output Format

```text
P0 必改：
P1 建议改：
P2 可优化：
标题改写：
缺失问题：
```
"""


def card_for_audience(name: str, body: str) -> str:
    dna = bullets_from(section(body, "表达DNA"), 6)
    values = bullets_from(section(body, "价值观与反模式"), 8)
    honest = bullets_from(section(body, "诚实边界"), 6)
    return f"""# Audience Card: {name}

## Profile

由 Nuwa Skill 自动导入。将该对象作为 PPT 受众画像或决策者画像使用。

## Attention Budget

- 默认前 3 页判断价值、可信度和是否值得继续听。
- 标题必须直接表达结论。
- 证据、场景、收益和风险应前置。

## Wants

{chr(10).join(f"- {item}" for item in (values[:6] or ["清晰结论、可信证据、可执行路径。"]))}

## Dislikes

{chr(10).join(f"- {item}" for item in (honest[:5] or ["空泛表达、过度承诺、缺少证据。"]))}

## Expression Clues

{chr(10).join(f"- {item}" for item in (dna[:5] or ["使用该对象易接受的表达节奏和关键词。"]))}

## First 3 Slides Test

1. 是否讲清为什么重要。
2. 是否讲清当前判断。
3. 是否讲清下一步行动或决策请求。
"""


def write_card(kind: str, name: str, content: str) -> Path:
    if kind == "reviewer":
        path = ROOT / "references" / "reviewers" / name / "reviewer-card.md"
    elif kind == "audience":
        path = ROOT / "references" / "audiences" / name / "audience-card.md"
    elif kind == "voice":
        path = ROOT / "references" / "voices" / name / "voice-card.md"
    else:
        raise ValueError(kind)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Nuwa skill zip or directory")
    parser.add_argument("--type", choices=["reviewer", "audience"], required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    name = slugify(args.name)
    text, temp_root = read_skill_md(Path(args.source))
    body = strip_frontmatter(text)

    if args.type == "reviewer":
        card = card_for_reviewer(name, body)
    else:
        card = card_for_audience(name, body)

    out = write_card(args.type, name, card)
    if temp_root.name.startswith("nuwa-skill-"):
        shutil.rmtree(temp_root, ignore_errors=True)
    print(out)
    print("Note: update registry.yml or run add_reviewer.py/add_audience.py to register this card.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
