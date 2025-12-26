# Hello World Skill

一个简单的示例技能包，用于演示Claude Code技能的基本结构。

## 📖 简介

Hello World是一个最小化的技能包示例，展示了如何创建和构建Claude Code技能。适合作为学习模板和参考。

## 🎯 功能

- 简单的问候响应
- 展示技能基本结构
- 提供开发模板

## 📦 安装

```bash
# 使用CLI工具安装
python scripts/marketplace.py install hello-world

# 或手动安装
cp -r skills/hello-world ~/.claude/skills/
```

## 🔧 使用

安装后，在Claude Code中：

```
hello
```

或

```
你好
```

技能将给出友好的回应。

## 📂 文件结构

```
hello-world/
├── SKILL.md         # 技能定义文件（必需）
├── README.md        # 使用说明
└── CHANGELOG.md     # 更新日志
```

## 🎓 学习要点

### SKILL.md结构

```yaml
---
name: hello-world                    # 技能名称
description: 技能描述                # 详细说明何时触发此技能
license: MIT                         # 许可证
---
```

**重要**:
- `description`字段是技能触发的关键
- 保持description清晰、具体
- 说明技能的使用场景和触发条件

### 主体内容

SKILL.md的主体部分包含：
- 功能说明
- 使用示例
- 实现细节
- 最佳实践

## 🚀 创建自己的技能

1. **复制模板**
   ```bash
   cp -r skills/hello-world skills/my-skill
   ```

2. **编辑SKILL.md**
   - 修改name
   - 更新description
   - 添加技能逻辑

3. **测试技能**
   - 安装技能
   - 在Claude Code中测试

4. **发布技能**
   - 提交到市场
   - 更新marketplace.json

## 📝 技能模板

### 简单技能

适用于单一功能的技能：

```markdown
---
name: my-simple-skill
description: 当用户需要[特定功能]时使用此技能。用于[使用场景]。
---
# 功能说明
...

# 使用示例
...
```

### 复杂技能

适用于多功能技能，需要包含：

```markdown
---
name: my-complex-skill
description: 全面的[领域]技能，涵盖[功能1]、[功能2]、[功能3]等多个方面。当用户需要[场景1]、[场景2]或[场景3]时使用此技能。
---

# 快速开始
...

# 功能列表
## 功能1
...

## 功能2
...

# 参考资源
...
```

## 🤝 贡献

欢迎基于此模板创建更多技能包！

## 📄 许可证

MIT License

---

**提示**: 查看其他技能包（如code-review-expert）了解更复杂的技能实现。
