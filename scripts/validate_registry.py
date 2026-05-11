#!/usr/bin/env python3
"""Validate ppt-director package integrity without external deps."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.yml"
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"


PATH_RE = re.compile(r"^\s+(?:path|slide_map|design_doc):\s+(.+?)\s*$")
ASSET_RE = re.compile(r"^\s+(?:contact_sheet|city_skyline):\s+(.+?)\s*$")

REQUIRED_WORKFLOWS = [
    "delivery-schema.md",
    "design-language-workflow.md",
    "director-workflow.md",
    "final-layout-review.md",
    "generation-ready-director-brief.md",
    "html-preview-to-pptx-workflow.md",
    "nuwa-to-ppt-workflow.md",
    "page-structure-brief-schema.md",
    "prompt-library.md",
    "visual-director-optimization.md",
]

REQUIRED_SKILL_PHRASES = [
    "页面描述_优化版",
    "生成就绪导演稿",
    "PPTX 实际渲染截图",
    "区域词",
    "主视觉占主体区",
    "字体字号",
    "城市剪影固定资产",
]

REQUIRED_README_PHRASES = [
    "页面描述优化",
    "生成就绪导演稿",
    "PPTX 实际渲染截图",
    "视觉一致版",
    "可编辑原生版",
    "字体字号",
    "city-skyline.png",
]

REQUIRED_REVIEW_PHRASES = [
    "模块间关系显性化",
    "主视觉与辅助内容的面积比",
    "流程路径页",
    "PPTX 实际渲染截图",
    "字体字号审查",
]

REQUIRED_DESIGN_PHRASES = [
    "微软雅黑 Light",
    "大标题",
    "36 / 44 / 60 / 72",
    "小标题",
    "20 / 24 / 28",
    "内容文字",
    "16 / 18",
    "city-skyline.png",
    "不得自行生成",
]

REQUIRED_GENERATION_READY_PHRASES = [
    "字体与字号参数",
    "大标题：36 / 44 / 60 / 72",
    "小标题：20 / 24 / 28",
    "内容文字：16 / 18",
    "城市剪影资产",
    "city-skyline.png",
]


def fail(message: str, details: list[str] | None = None) -> int:
    print(f"FAIL {message}")
    for item in details or []:
        print(f"- {item}")
    return 1


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_skill_frontmatter() -> list[str]:
    if not SKILL.exists():
        return [f"missing SKILL.md: {SKILL}"]

    text = read(SKILL)
    if not text.startswith("---\n"):
        return ["SKILL.md missing YAML frontmatter"]
    try:
        frontmatter = text.split("---", 2)[1]
    except IndexError:
        return ["SKILL.md frontmatter is not closed"]

    errors: list[str] = []
    if len(frontmatter) > 1024:
        errors.append(f"frontmatter too long: {len(frontmatter)} chars")

    desc_match = re.search(r"description:\s*(?:\|\s*)?\n((?:\s+.+\n?)+)", frontmatter)
    if not desc_match:
        errors.append("frontmatter missing multiline description")
    else:
        desc = " ".join(line.strip() for line in desc_match.group(1).splitlines()).strip()
        if not desc.startswith("Use when "):
            errors.append("description must start with 'Use when ' and describe trigger conditions")
        blocked = ["用于从", "规划并生成", "支持默认", "也支持导入"]
        found = [phrase for phrase in blocked if phrase in desc]
        if found:
            errors.append("description summarizes workflow/process instead of triggers: " + ", ".join(found))
    return errors


def missing_phrases(path: Path, phrases: list[str]) -> list[str]:
    if not path.exists():
        return [f"missing file: {path}"]
    text = read(path)
    return [f"{path.relative_to(ROOT)} missing phrase: {phrase}" for phrase in phrases if phrase not in text]


def main() -> int:
    if not REGISTRY.exists():
        return fail(f"missing registry: {REGISTRY}")

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
        return fail("missing registry targets:", [str(path) for path in missing])

    errors: list[str] = []
    errors.extend(validate_skill_frontmatter())
    errors.extend(missing_phrases(SKILL, REQUIRED_SKILL_PHRASES))
    errors.extend(missing_phrases(README, REQUIRED_README_PHRASES))

    workflow_dir = ROOT / "references" / "workflows"
    for name in REQUIRED_WORKFLOWS:
        target = workflow_dir / name
        if not target.exists():
            errors.append(f"missing workflow: {target.relative_to(ROOT)}")

    errors.extend(missing_phrases(workflow_dir / "final-layout-review.md", REQUIRED_REVIEW_PHRASES))
    errors.extend(
        missing_phrases(ROOT / "references" / "styles" / "digital-zhejiang" / "design.md", REQUIRED_DESIGN_PHRASES)
    )
    errors.extend(missing_phrases(workflow_dir / "generation-ready-director-brief.md", REQUIRED_GENERATION_READY_PHRASES))

    ds_store = [path.relative_to(ROOT) for path in ROOT.rglob(".DS_Store")]
    if ds_store:
        errors.extend(f"remove macOS metadata file: {path}" for path in ds_store)

    if errors:
        return fail("package integrity checks:", errors)

    print(f"PASS registry targets: {len(checked)}")
    print("PASS package integrity checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
