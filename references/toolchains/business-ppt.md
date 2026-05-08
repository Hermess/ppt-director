# Toolchain: business-ppt

## Use When

业务汇报、数据分析、政务汇报、国企项目汇报、培训课件、项目总结。

## Priority

1. 逻辑清晰。
2. 数据准确。
3. 标题有观点。
4. 版式稳定。
5. 风格一致。

## Recommended Execution

- 优先生成标准交付文档。
- 使用 python-pptx、artifact-tool 或 Marp 生成文件。
- 数据图表使用原始数据生成，不手工编造。
- 图片没有准备好时使用明确占位符路径。
- 每个页面函数化，方便局部修改。

## Coding Agent Prompt Addendum

```text
这是业务型 PPT。请优先保证逻辑、信息层级、数据图表和可读性。
不要为了视觉效果牺牲文字清晰度。
每页标题必须可单独串成故事线。
代码结构请按页拆分函数，便于后续针对单页修改。
```
