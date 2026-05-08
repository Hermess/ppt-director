# Toolchain: visual-ppt

## Use When

发布会、品牌展示、融资路演、大会 keynote、强视觉冲击演示。

## Priority

1. 画面冲击力。
2. 视觉一致性。
3. 文字可读性。
4. 叙事节奏。
5. 文件可编辑性。

## Recommended Execution

- 先确认每页是否需要 AI 生图。
- 生成图片 Prompt 时要指定构图留白、主色、禁忌元素。
- 图片页用全屏背景图，文字叠加半透明色块。
- 非图片页使用统一渐变或纯色大字页。
- 每张图要检查是否有文字乱码、人物误生成、品牌伪造。

## Image Prompt Schema

```text
页面：
内容：
用途：背景图 / 配图 / 主视觉
风格：
色调：
构图留白：
禁忌：
中文 Prompt：
English Prompt：
```

## Coding Agent Prompt Addendum

```text
这是强视觉 PPT。请将图片作为视觉主角，代码负责排版、文字层级和文件组装。
图片页必须保证文字在背景上清晰可读。
不要生成虚假 logo、虚假截图、虚假产品界面。
```
