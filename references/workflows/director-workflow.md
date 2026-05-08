# PPT Director Workflow

## A. 灵感激发

适用：用户只有主题、模糊目标或零散素材。

动作：

- 明确主题、受众、目的、时长、已有素材。
- 如果已有 audience-card，直接用受众视角提问。
- 如果没有 audience-card，生成女娲受众蒸馏 Prompt。
- 输出核心信息、受众关切、前 3 页必须讲清楚的内容、2-3 种叙事结构。

## B. 内容打磨

适用：核心思路已确定，需要变成 PPT 大纲。

动作：

- 生成页数预算。
- 每页写观点型标题。
- 每页写 3-5 个要点。
- 标注图表页、图片页、结构图页、纯文字页。
- 标注需要 AI 生图的页面。
- 输出标准交付文档。

## C. 视觉定义

适用：内容已基本确定，需要决定风格和页型。

动作：

- 读取当前 style-card。
- 读取 slide-type-map，把每页内容映射到模板页型。
- 判断是业务 PPT 还是酷炫视觉 PPT。
- 若需要 AI 图片，生成图片 Prompt。

## D. 代码生成

适用：已有标准交付文档和风格说明，需要实际 PPT 文件。

动作：

- 读取当前 toolchain。
- 生成给 Codex / Claude Code / OpenClaw 的执行 Prompt。
- 建议优先使用 python-pptx 或 artifact-tool 生成 PPTX。
- 生成后必须检查预览或至少做布局自查。

## E. 迭代优化

适用：已有大纲、标准交付文档或初稿 PPT。

动作：

- Audience check：受众是否关心，前 3 页是否有效。
- Reviewer check：专家是否认可逻辑、抓手、风险闭环。
- Style check：风格是否统一、页型是否匹配。
- 输出 `P0/P1/P2` 修改清单。

## Path Presets

### quick

输出：页数规划、每页标题、3 个要点、视觉建议。

### controlled

输出：受众校准、大纲、逐页内容、风格映射、评审修改清单。

### premium

输出：受众蒸馏、完整标准交付文档、视觉定义、生图 Prompt、代码生成 Prompt、专家评审。
