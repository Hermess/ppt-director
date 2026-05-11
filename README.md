# PPT Director 技能包

PPT Director 是一个可插拔的 PPT 总导演 Skill，用来把“主题/素材/受众画像/评审专家/设计语言/HTML 预览/PPTX 生成/最终审查”串成一条可执行的演示文稿生产线。

它的定位不是简单代写 PPT，而是帮助模型先把页面结构想清楚，再按指定设计语言生成 HTML 预览，经审查通过后再映射为可编辑 PPTX。

## 适用场景

- 政务汇报、数字化改革汇报、公共数据/知识库/一网通办/一网通管解决方案
- 产品解决方案、客户提案、项目总结、培训课件
- 创业 BP、发布会 keynote、研究报告转 PPT
- 需要结合女娲对象 Skill、专家评审 Skill、指定 PPT 设计语言生成高质量材料的场景

## 核心工作流

```text
受众/专家视角校准
  -> 内容规划 MD
  -> PPT 视觉导演优化 MD
  -> 选择设计语言并对表 design.md / 截图样例
  -> 合成生成就绪导演稿（输出格式 / 画布 / 坐标 / 样式 token / 组件映射）
  -> 生成 HTML 预览和 contact sheet
  -> 产品解决方案专家 + PPT 专家双视角审查
  -> 审查通过后映射为 PPTX
  -> 导出 PPTX 实际渲染截图并与 HTML/PNG 对比
  -> 再审查，通过后输出
```

## 快速安装

将本目录或压缩包安装到 Codex/Claude Code/OpenClaw 等支持 Skill 的工作台中即可。

推荐依赖：

```bash
pip install python-pptx Pillow
npx skills add alchaincyf/nuwa-skill
npx skills add alchaincyf/darwin-skill
```

说明：

- 女娲 Skill 不内置在本包中，建议单独安装，用于蒸馏受众画像、评审专家、人物视角。
- 达尔文 Skill 不内置在本包中，建议单独安装，用于重要 PPT 的多轮内容优化。
- PPT Director 负责把这些对象 Skill 和 PPT 设计语言串起来，执行完整生成流程。

## 30 秒快速使用

```text
使用 $ppt-director 帮我生成一份 PPT。

主题：全省知识库平台解决方案
受众：X 省数据局/政务服务相关领导
目的：作为解决方案推销我们的产品
素材：参考我提供的 PPT、产品截图、测评页和补充要求
设计语言：digital-zhejiang
评审专家：jin-zhipeng-perspective

请先输出 PPT 内容规划 MD；
再以产品解决方案专家 + PPT 视觉专家视角优化成页面结构导演稿；
然后读取 digital-zhejiang 的 design.md、style-card、slide-type-map 和截图样例生成 HTML 预览；
HTML 经审查通过后，再映射生成 PPTX。
```

## 推荐输入材料

- 主题、受众、演讲目的、时长、页数范围
- 原始 PPT、Word、PDF、图片、产品截图、数据表
- 必须保留的业务边界、产品能力、场景要求、政策依据
- 想使用的受众 Skill、评审专家 Skill、设计语言包
- 不希望出现的表达方式，例如“不要普通卡片堆叠”“不要把左侧/右侧写进页面文案”

## 页面内容 MD 规范

进入 HTML/PPTX 生成前，每一页必须先经过“页面描述优化”。用户给的原始 MD 只作为事实来源，不能直接生成 HTML/PPTX。优化版页面描述建议按下面结构描述：

```markdown
# 页面标题

# 本页核心结论

# 页面类型
分层架构页 / 业务流程页 / 能力体系页 / 对比分析页 / 场景价值页 / 实施路径页 / 案例成效页 / 机制说明页

# 页面版式
- 16:9 PPT 单页
- 顶部：
- 主体：
- 底部：
- 信息密度：

# 主视觉设计
这一页主要用什么图表达，主视觉承担什么解释逻辑。

# 主视觉内容
## 区域/步骤 1
-

## 区域/步骤 2
-

# 模块间关系
- 主模块：
- 辅助模块：
- 关系类型：并列 / 支撑底座 / 总分 / 贯穿型能力 / 侧挂治理层
- 表达方式：

# 主视觉与辅助内容面积预算
- 主视觉占主体区：
- 辅助模块占比：
- 是否存在双主视觉冲突：

# 页面文案
只写真正上屏的短文案。

# 页面想表达的管理价值
-
-
-

# 页面底部总结语
价值：

# 生成风险提示
- 模块关系不清：
- 主视觉占比不足：
- 贯穿型能力位置错误：
- 箭头关系不清：

# 出图要求
- 中文清晰
- 主视觉优先，文字辅助
- 不要文字过密
- 不要普通模板页
```

注意：

- `左侧：`、`右侧：`、`顶部：`、`底部：` 这类词是排版指令，不是上屏文案。生成 HTML 和 PPTX 时必须清洗掉这些区域前缀。
- 页面必须有 1 个明确主视觉，主视觉占主体区建议不低于 55%。
- 流程路径页中，流程主视觉应占主体区 60% 以上；价值点只做底部收束或侧边点缀，不超过 3 条。
- 监测中心、审核中心、安全中心等贯穿型能力，应作为底座、背景条、侧挂治理层或护栏，不要塞在流程中间。

## 生成就绪导演稿

页面描述优化版解决“讲什么、怎么组织”，但还不能直接生成。进入 HTML/PPTX 前，需要再生成一份“生成就绪导演稿”，把设计系统也读进来。

默认产物命名建议为：

```text
[项目名]_生成就绪导演稿.md
```

例如 `平台边界双向流转_生成就绪导演稿.md`。HTML、PNG、PPTX 生成时，应以这份导演稿作为代码 Agent 的直接输入。

它必须包含：

- 输出格式：HTML+CSS、SVG、python-pptx 或 HTML+PPTX
- 画布参数：1280×720、标题区、主体区、底部区、安全边距
- 设计系统 token：来自 `design.md` 的颜色、字体、母版元素、组件形态、线条和箭头样式
- 字体字号参数：字体、字号档位、字重，以及每个组件的字体 / 字号 / 字重
- 固定资产引用：来自 `registry.yml` 和 `design.md` 的母版资产路径，例如 `city-skyline.png`
- 区域坐标或比例：主视觉区、侧挂模块、底部价值区
- 组件映射：内容节点 -> 设计系统组件 -> 坐标/尺寸 -> 样式 token
- 连接规则：箭头起点、终点、方向、禁止连接
- 生成优先级：主视觉面积和关系正确优先于局部美观

这样做的好处是：页面结构稿仍然可以换风格，真正生成时又不会缺少坐标、尺寸、色彩、字号和箭头参数。

## 设计语言机制

默认内置 `digital-zhejiang` 设计语言，来源于数字浙江 PPT 模板抽象。生成时不会机械照抄某一页截图，而是读取以下文件进行风格对齐：

```text
references/styles/digital-zhejiang/design.md
references/styles/digital-zhejiang/style-card.md
references/styles/digital-zhejiang/slide-type-map.md
references/styles/digital-zhejiang/contact-sheet.png
references/styles/digital-zhejiang/assets/city-skyline.png
```

如果要替换 PPT 风格，可以新增一个设计语言目录，并在 `registry.yml` 中注册。最低要求：

```text
design.md
style-card.md
slide-type-map.md
contact-sheet.png 或若干截图样例
```

## digital-zhejiang 字体字号规则

内置数字浙江风格默认使用以下字体字号规范。生成就绪导演稿必须把这些规则落到组件级，不能只写“正式、简洁、政务风”。

- 主字体：微软雅黑
- 允许字重：Regular / Bold
- 大标题：36 / 44 / 60 / 72，Bold
- 小标题：20 / 24 / 28，Bold
- 内容文字：16 / 18，Regular 或 Bold
- 页脚/来源：12 / 14 / 16，Regular
- 禁止：微软雅黑 Light、宋体、特殊字体

审查时要确认 HTML 和 PPTX 实际渲染图都满足上述档位。若 PPTX 因字体替换导致换行、溢出、遮挡或字号被压低，不能通过最终审查。

## digital-zhejiang 固定母版资产

正文页右下城市背景装饰使用固定 PNG 资产：

```text
references/styles/digital-zhejiang/assets/city-skyline.png
```

生成 HTML/PPTX 时必须直接引用该资产，保持透明背景、宽高比和右下锚定。不要让模型自行生成城市剪影，不要用 CSS/SVG 重绘，不要替换为照片、卡通或其他城市图。

## 目录结构

```text
ppt-director/
├── SKILL.md
├── README.md
├── registry.yml
├── agents/
├── references/
│   ├── audiences/        # 受众画像
│   ├── reviewers/        # 评审专家
│   ├── styles/           # PPT 设计语言
│   ├── templates/        # 卡片模板
│   ├── toolchains/       # 生成工具链
│   └── workflows/        # 工作流、页面规范、审查规范
└── scripts/
```

## 关键内置规范

- `references/workflows/page-structure-brief-schema.md`：PPT 单页内容描述规范
- `references/workflows/visual-director-optimization.md`：内容 MD 到视觉导演 MD 的优化步骤
- `references/workflows/generation-ready-director-brief.md`：读取设计系统后的生成就绪导演稿
- `references/workflows/html-preview-to-pptx-workflow.md`：先 HTML 后 PPTX 的生成流程
- `references/workflows/final-layout-review.md`：最终页面布局审查规范
- `references/workflows/design-language-workflow.md`：设计语言选择和对表流程

## PPTX 视觉一致性规则

PPTX 不是“能打开”就算通过。生成 PPTX 后必须导出实际渲染截图，并与已确认的 HTML/PNG 预览并排对比。

必须检查：

- 标题、判断句和模块文字是否换行或溢出
- 字体是否仍为微软雅黑或合规替代，字号是否落在设计档位，是否因字体替换导致换行/溢出
- 右下城市剪影是否直接引用 `city-skyline.png`，而不是模型新画或代码重绘
- 箭头方向、连接点和模块关系是否正确
- 主视觉是否仍然是页面中心，辅助内容是否没有抢视觉
- 母版元素、页脚、安全区、角标是否没有漂移
- `左侧/右侧/顶部/底部/中部/侧边` 等区域词是否没有误上屏

如果原生可编辑 PPTX 渲染后明显偏离预览，优先修复原生映射。短期无法修复且用户更重视演示效果时，输出两个版本：

- `视觉一致版`：整页或局部栅格化，保证与 HTML/PNG 预览一致
- `可编辑原生版`：文本和形状可编辑，但标明仍需人工校准

交付时必须说明最终采用哪个版本，不能把视觉错误的可编辑 PPTX 当作最终成稿。

## 校验技能包

```bash
python3 scripts/validate_registry.py
```

若输出 `PASS registry targets`，说明 `registry.yml` 中注册的受众、评审专家、设计语言、工具链文件都能正确找到。

## English Reference

# PPT Director

PPT Director is a pluggable Skill for producing high-quality presentations from a topic, audience model, expert reviewer, page structure brief, design language, and code-generation toolchain.

It is designed for workflows where the presentation must fit a specific audience and review standard, not just “look like a PPT”.

## Core Idea

```text
Nuwa creates cognitive models.
Darwin improves the content plan.
PPT Director orchestrates the production line.
Codex / Claude Code / OpenClaw generates HTML preview and the PPT file.
```

PPT Director does not replace Nuwa or Darwin. It connects them.

The newest version separates content structure from visual style:

1. A **page structure brief** for every slide. This brief describes what the slide says, how information is organized, module placement, main visual logic, side modules, node text, value tags, bottom summary, and output constraints.
2. A **visual director optimization pass** between content MD and HTML generation. Product solution and PPT visual expert perspectives rewrite the content into a stronger page storyboard without changing business facts or binding a visual style.
3. A **design language crosswalk** before generation. The user chooses a design language, then PPT Director aligns the deck against its `design.md`, `style-card.md`, `slide-type-map.md`, and screenshot/contact-sheet examples.
4. A **final layout gate** for both HTML and PPTX. Product solution experts check business value and scenario closure; PPT experts check layout, density, main visual expression, and readability.

Page structure briefs must not contain specific design-language names, colors, fonts, master elements, or screenshot references. Screenshot examples are used only during generation for style alignment, not forced copying.

Layout-region words in a page structure brief are instructions, not visible copy. If a section is written as `左侧：公共数据共享平台` or `右侧：业务场景`, generated HTML/PPTX should show `公共数据共享平台` and `业务场景`, not the region prefix.

| Component | Role | Typical Output |
| --- | --- | --- |
| Nuwa Skill | Distill audience or expert cognition | `audience.skill`, `expert.skill` |
| Darwin Skill | Iteratively optimize content | optimized content plan |
| PPT Director | Route workflow, apply design language, gate deliverables | `delivery-doc`, `html-preview`, `pptx`, review report |
| Coding agent | Write and run HTML/PPT generation code | `.html`, screenshots, `.pptx` |

## Default Setup

This repository ships with a default government digital-reporting setup:

- Audience: `default-government-leader`
- Reviewer: `yuan-jiajun`
- Design language: `digital-zhejiang`
- Toolchain: `business-ppt`

The default visual style is based on a blue-white “Digital Zhejiang” presentation system:

- main blue `#014EC6`
- accent orange `#FFAA11`
- Microsoft YaHei typography
- white content pages
- deep-blue geometric cover and closing pages
- title, architecture, matrix, numbered list, circular relation, logo wall, and QR-code slide patterns

Each design language can include:

```text
design.md          # full design system: visual DNA, master elements, layout language, rules
style-card.md      # short model-facing summary
slide-type-map.md  # content type -> slide type mapping
contact-sheet.png  # screenshot/contact-sheet reference, optional
```

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

Use the default digital-zhejiang design language and yuan-jiajun reviewer.
First produce a standard delivery document with page structure briefs. Then confirm the design language and prepare a PPTX generation plan.
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

Ask PPT Director to combine the topic, audience card, and reviewer card into a reusable page structure plan.

```text
Use $ppt-director with:
- audience: [audience-card name]
- reviewer: [reviewer-card name]
Create a page-by-page plan for a [X]-minute PPT about [topic].
Each page must include:
1. opinionated title
2. core point
3. supporting data or case
4. visual direction
5. audience psychology
6. transition logic
7. page structure brief: layout, main visual, module content, expression guidance, value tags, and output constraints
```

Output:

```text
content-plan.md
```

### 3.5 Choose And Crosswalk The Design Language

Before writing PPTX code, confirm which design language to use.

```text
Use $ppt-director.

Design language: digital-zhejiang

Please read:
- design.md
- style-card.md
- slide-type-map.md
- contact-sheet.png

Produce a design language crosswalk before generation:
1. core visual DNA
2. fixed master elements
3. allowed variants
4. forbidden deviations
5. slide-by-slide page type mapping
```

Important rule:

```text
Do not force every page to match a screenshot layout.
Use screenshots as style references.
If a page naturally matches a sample page type, align it.
If the content needs a variant, keep colors, typography, master elements, component grammar, and information density consistent with design.md.
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

### 4.5 Add Page Structure Briefs

Before generating PPTX, make sure every page has a structure brief:

```text
For every page in optimized-delivery-doc.md, add a page structure brief.

Each page must include:
- page title
- core conclusion
- layout
- top judgement sentence
- central main visual
- module/stage/area content
- design suggestions
- bottom value tags
- bottom summary sentence
- output constraints

Do not write vague instructions like "make a flowchart".
Describe the direction, module positions, node text, information hierarchy, and what should not appear on screen.
Do not include design-language names, colors, fonts, master elements, or screenshot references in the page structure brief.
Treat words such as `left side`, `right side`, `top`, `bottom`, `左侧`, `右侧`, `顶部`, `底部`, `中部`, and `侧边` as layout instructions. Do not display those prefixes as module titles.
```

Reference schema:

```text
references/workflows/page-structure-brief-schema.md
```

### 4.6 Run Visual Director Optimization

Before HTML generation, run the visual director pass if the current file is still a content-style PPT MD:

```text
Use $ppt-director to optimize content-plan.md into a visual-director MD.

Requirements:
- do not change business facts
- do not drop required materials, links, product abilities, metrics, or scenarios
- strengthen page type, layout skeleton, main visual, on-screen copy, and management value
- keep concrete design language, colors, fonts, master elements, and screenshots out of the MD
- treat layout-region words as instructions, not visible copy
```

Reference workflow:

```text
references/workflows/visual-director-optimization.md
```

### 5. Generate HTML Preview First

Use PPT Director with a toolchain.

Business deck:

```text
Use $ppt-director to generate an HTML design preview from optimized-delivery-doc.md.

Toolchain: business-ppt
Design language: digital-zhejiang
Output: HTML preview + contact sheet

Requirements:
- use page structure brief as the content/layout source
- use the visual-director optimized MD when available
- use design.md as the visual style source
- align with design.md and contact-sheet style references
- do not force every page to copy screenshot layouts
- generate per-slide screenshots and a contact sheet
- run final-layout-review.md using product solution expert + PPT expert perspectives
- clean layout-region prefixes before rendering visible text
- if score is below 80 or any P0 issue exists, revise HTML before continuing
```

### 5.5 Map Confirmed HTML To PPTX

Only after the HTML preview passes final layout review and the user confirms it:

```text
Use $ppt-director to map the approved HTML preview to editable PPTX.

Requirements:
- do not default to full-page screenshots
- preserve editable text, rectangles, arrows, matrices, flows, and layer structures where practical
- rasterize only complex local visuals or screenshots
- export preview screenshots from the PPTX
- run final-layout-review.md again before delivery
- only output final PPTX if score >= 80 and there are no P0 issues
```

Visual/keynote deck:

```text
Use $ppt-director with toolchain visual-ppt.
First list image-generation prompts for every slide that needs a strong visual.
After I provide image paths, generate and run the PPTX code.
```

### 6. Review From Audience, Product Solution, And PPT Perspectives

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

Final delivery also requires:

```text
Use final-layout-review.md to review HTML/PPTX with:
1. product solution expert perspective
2. PPT expert perspective
3. current design language perspective

Do not mark the deck as final if score < 80 or any P0 issue remains.
```
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
- 页面结构导演稿：
- 演讲备注：

【生成配置（仅代码生成阶段使用）】
- 设计语言：
- 设计系统文档：
- 样例截图/Contact Sheet：
- style-card：
- slide-type-map：

【HTML设计预览配置】
- HTML输出目录：
- 每页截图目录：
- Contact Sheet：
- HTML最终布局审查报告：
- 是否已通过HTML审查：

【PPTX映射配置】
- 映射来源HTML：
- PPTX输出路径：
- PPTX最终布局审查报告：
- 是否已通过PPTX审查：
```

See `references/workflows/delivery-schema.md` for the full format.

## Extending PPT Director

PPT Director is intentionally registry-driven.

### Add A Style

Prepare:

```text
design.md
style-card.md
slide-type-map.md
contact-sheet.png optional
```

Run:

```bash
python scripts/add_style.py \
  --name mckinsey-blue \
  --design-doc /path/to/design.md \
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
PASS registry targets: 8
```

## Best Practices

- Use Nuwa when the audience or expert lens matters.
- Use Darwin for important decks that need stronger persuasion.
- Use PPT Director for orchestration and standardization.
- Keep styles, audiences, reviewers, and toolchains separate.
- Always confirm the design language before PPT generation.
- Generate HTML preview and contact sheet before PPTX unless the user explicitly asks for a quick draft.
- Run final layout review on both HTML and PPTX; product solution expert and PPT expert perspectives are mandatory.
- Do not deliver a final deck when the final layout review score is below 80 or P0 issues remain.
- Keep page structure briefs free of concrete style tokens.
- Do not put layout-region labels such as `左侧：`, `右侧：`, `顶部：`, `底部：`, `中部：`, or `侧边：` onto slides as visible copy.
- Align generated slides with `design.md`; use screenshot examples for style calibration, not rigid page copying.
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
