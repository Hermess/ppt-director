# PPT Director

PPT Director is a pluggable Skill for producing high-quality presentations from a topic, audience model, expert reviewer, visual style, and code-generation toolchain.

It is designed for workflows where the presentation must fit a specific audience and review standard, not just “look like a PPT”.

## Core Idea

```text
Nuwa creates cognitive models.
Darwin improves the content plan.
PPT Director orchestrates the production line.
Codex / Claude Code / OpenClaw generates the PPT file.
```

PPT Director does not replace Nuwa or Darwin. It connects them.

| Component | Role | Typical Output |
| --- | --- | --- |
| Nuwa Skill | Distill audience or expert cognition | `audience.skill`, `expert.skill` |
| Darwin Skill | Iteratively optimize content | optimized content plan |
| PPT Director | Route workflow, apply style, generate deliverables | `delivery-doc`, `pptx`, generation prompt |
| Coding agent | Write and run PPT generation code | `.pptx` |

## Default Setup

This repository ships with a default government digital-reporting setup:

- Audience: `default-government-leader`
- Reviewer: `yuan-jiajun`
- Style: `digital-zhejiang`
- Toolchain: `business-ppt`

The default visual style is based on a blue-white “Digital Zhejiang” presentation system:

- main blue `#014EC6`
- accent orange `#FFAA11`
- Microsoft YaHei typography
- white content pages
- deep-blue geometric cover and closing pages
- title, architecture, matrix, numbered list, circular relation, logo wall, and QR-code slide patterns

## Repository Structure

```text
ppt-director/
├── SKILL.md
├── registry.yml
├── agents/
│   └── openai.yaml
├── references/
│   ├── audiences/
│   ├── reviewers/
│   ├── styles/
│   ├── templates/
│   ├── toolchains/
│   └── workflows/
└── scripts/
    ├── add_audience.py
    ├── add_reviewer.py
    ├── add_style.py
    ├── import_nuwa_skill.py
    └── validate_registry.py
```

## Installation

Install this folder as a Codex/Claude-compatible Skill using your local Skill installer.

If your environment supports installing a local Skill directory, install the `ppt-director/` folder directly.

If your environment supports zip packages, zip the folder and install that package.

Recommended optional dependencies for PPT generation:

```bash
pip install python-pptx Pillow
npx skills add alchaincyf/nuwa-skill
npx skills add alchaincyf/darwin-skill
```

Nuwa and Darwin are intentionally not bundled in this repository. Install them separately so they can be upgraded and reused outside PPT workflows.

## Quick Start

Ask your coding agent:

```text
Use $ppt-director to create a PPT.

Topic: [your topic]
Audience: [who will watch it]
Goal: [what decision or understanding you want]
Duration: [X minutes]
Materials: [paste or describe source material]

Use the default digital-zhejiang style and yuan-jiajun reviewer.
First produce a standard delivery document, then prepare a PPTX generation plan.
```

## Full Workflow

### 1. Distill The Audience With Nuwa

Use Nuwa when the presentation depends on decision-maker psychology.

Example:

```text
Use Nuwa to distill a cognitive model for a CFO reviewing a 5 million RMB IT budget request.
Focus on decision criteria, rejection triggers, preferred evidence, and what the first 3 slides must answer.
```

Output:

```text
audience.skill.md
```

Import it into PPT Director as an audience card.

### 2. Distill An Expert Reviewer

Use Nuwa to create an expert perspective for review and critique.

Example:

```text
Use Nuwa to distill Nancy Duarte as a presentation design reviewer.
Focus on narrative structure, slide signal-to-noise ratio, emotional pacing, and title rewriting rules.
```

Output:

```text
expert.skill.md
```

Import it into PPT Director as a reviewer card.

### 3. Generate A Content Plan

Ask PPT Director to combine the topic, audience card, reviewer card, and style card.

```text
Use $ppt-director with:
- audience: [audience-card name]
- reviewer: [reviewer-card name]
- style: digital-zhejiang

Create a page-by-page plan for a [X]-minute PPT about [topic].
Each page must include:
1. opinionated title
2. core point
3. supporting data or case
4. visual direction
5. audience psychology
6. transition logic
```

Output:

```text
content-plan.md
```

### 4. Optimize With Darwin

For important decks, optimize the content plan before generating files.

```text
Use Darwin to optimize content-plan.md.

Goals:
- persuasiveness
- logical clarity
- information density
- audience fit

Constraints:
- keep within [X] slides
- keep within [X] minutes
- data must remain verifiable
```

Output:

```text
optimized-delivery-doc.md
```

### 5. Generate The PPT

Use PPT Director with a toolchain.

Business deck:

```text
Use $ppt-director to generate a PPTX from optimized-delivery-doc.md.

Toolchain: business-ppt
Style: digital-zhejiang
Output: presentation.pptx

Requirements:
- 16:9 widescreen
- Microsoft YaHei
- main color #014EC6
- accent color #FFAA11
- editable slides
- run the generated code and report the output path
```

Visual/keynote deck:

```text
Use $ppt-director with toolchain visual-ppt.
First list image-generation prompts for every slide that needs a strong visual.
After I provide image paths, generate and run the PPTX code.
```

### 6. Review From Audience And Expert Perspectives

```text
Use $ppt-director to review the final PPT with:
1. [audience-card] as the audience perspective
2. [reviewer-card] as the expert perspective

For each slide, output:
- first reaction
- unanswered question
- trust issue
- score from 1 to 10
- required change
```

## Standard Delivery Document

Before code generation, PPT Director should normalize content into this interface:

```text
【PPT信息】
- 标题：
- 副标题：
- 受众：
- 目的：
- 时长：
- PPT类型：业务PPT / 酷炫视觉PPT
- 风格：
- 评审专家：
- 核心信息：
- 输出方式：

【逐页内容】
第1页 | 类型：封面
- 标题：
- 副标题：
- 要点：
- 数据/图表需求：
- 视觉需求：
- 推荐页型：
- 演讲备注：
```

See `references/workflows/delivery-schema.md` for the full format.

## Extending PPT Director

PPT Director is intentionally registry-driven.

### Add A Style

Prepare:

```text
style-card.md
slide-type-map.md
contact-sheet.png optional
```

Run:

```bash
python scripts/add_style.py \
  --name mckinsey-blue \
  --style-card /path/to/style-card.md \
  --slide-map /path/to/slide-type-map.md \
  --contact-sheet /path/to/contact-sheet.png \
  --use-when "consulting reports, strategy analysis, management presentations"
```

### Add A Reviewer

```bash
python scripts/add_reviewer.py \
  --name duarte \
  --card /path/to/reviewer-card.md \
  --use-when "narrative presentations, keynote speeches, product launches"
```

### Add An Audience

```bash
python scripts/add_audience.py \
  --name cfo-budget-reviewer \
  --card /path/to/audience-card.md \
  --use-when "budget approval, ROI review, finance decision"
```

### Import A Nuwa Skill

```bash
python scripts/import_nuwa_skill.py \
  /path/to/yuan-jiajun-perspective.zip \
  --type reviewer \
  --name yuan-jiajun
```

The import script creates a card. Register it with `add_reviewer.py` or update `registry.yml`.

## Validate

```bash
python scripts/validate_registry.py
```

Expected output:

```text
PASS registry targets: 7
```

## Best Practices

- Use Nuwa when the audience or expert lens matters.
- Use Darwin for important decks that need stronger persuasion.
- Use PPT Director for orchestration and standardization.
- Keep styles, audiences, reviewers, and toolchains separate.
- Do not hard-code one expert or one visual style into `SKILL.md`.
- Prefer a standard delivery document before generating PPT files.

## Limitations

- `python-pptx` is good for structure, content, charts, and basic layout, but not advanced animation.
- Brand-grade visual polish may still need final manual adjustment in PowerPoint or Keynote.
- AI-generated images should be checked for text artifacts, fake logos, and inconsistent style.
- For strict brand templates, provide a real `.pptx` template and reuse its layouts.

## One-Line Summary

```text
Nuwa creates the thinking models.
Darwin improves the content.
PPT Director orchestrates the deck.
The coding agent generates the file.
```
