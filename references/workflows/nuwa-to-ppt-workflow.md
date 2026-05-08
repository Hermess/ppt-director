# Nuwa To PPT Workflow

女娲 Nuwa 的角色是生成“对象 Skill”：受众、专家、人物视角、表达风格。PPT Director 不内置女娲本体，只把女娲产物转换成 PPT 可用插件。

## Import Targets

### Audience Card

当女娲 Skill 描述的是目标观众、领导、客户、评委、投资人时，转换为 audience-card。

抽取字段：

- 角色身份
- 关注焦点
- 决策风格
- 注意力预算
- 最想看到什么
- 最反感什么
- 前 3 页判断标准
- 可能追问的问题

### Reviewer Card

当女娲 Skill 描述的是专家、领导、行业人物或某种评审视角时，转换为 reviewer-card。

抽取字段：

- 评审镜头
- 关注重点
- 反模式
- 标题改写规则
- 结构审查清单
- 风险审查清单
- 输出格式

### Voice Card

当用户希望 PPT 采用某类表达语气时，可转换为 voice-card。

抽取字段：

- 表达 DNA
- 常用词汇
- 句式节奏
- 禁忌表达
- 标题语言规则

## Recommended Flow

1. 用户提供 Nuwa skill zip 或目录。
2. 解压并读取 `SKILL.md`。
3. 判断导入类型：audience / reviewer / voice。
4. 按模板生成卡片。
5. 放入对应目录。
6. 更新 `registry.yml`。
7. 后续 PPT 生成只读取轻量卡片，不加载完整 Nuwa Skill。

## User Prompt Template

```text
我上传了一个女娲生成的对象 Skill。
请把它导入 PPT Director：
- 作为受众画像 / 评审专家 / 表达风格
- 名称：
- 默认是否启用：
```
