# Claude Code Skills 开发规范

## 📋 目录

1. [Skill基本结构](#skill基本结构)
2. [SKILL.md规范](#skillmd规范)
3. [文件命名规范](#文件命名规范)
4. [内容编写规范](#内容编写规范)
5. [代码质量规范](#代码质量规范)
6. [文档规范](#文档规范)
7. [最佳实践](#最佳实践)
8. [提交审核清单](#提交审核清单)

---

## Skill基本结构

### 最小结构

每个Skill必须包含：

```
skill-name/
├── SKILL.md          # 必需：技能定义文件
```

### 推荐结构

```
skill-name/
├── SKILL.md                    # 必需：技能定义
├── README.md                   # 必需：使用说明
├── CHANGELOG.md                # 推荐：更新日志
├── LICENSE                     # 可选：许可证（推荐MIT）
├── references/                 # 可选：参考资料
│   ├── topic1.md
│   └── topic2.md
├── scripts/                    # 可选：辅助脚本
│   └── tool.py
└── assets/                     # 可选：资源文件
    └── template.md
```

### 目录要求

- **所有文件使用UTF-8编码**
- **行尾符统一使用LF**（避免CRLF）
- **文件名使用小写字母和连字符**（kebab-case）
- **避免使用空格和特殊字符**

---

## SKILL.md规范

### 1. Frontmatter（必需）

SKILL.md文件开头必须包含YAML frontmatter：

```yaml
---
name: skill-name                    # 必需：技能名称（唯一标识）
description: 详细描述...           # 必需：何时使用此技能
license: MIT                        # 推荐：许可证
---
```

#### 字段说明

**name** (必需)
- 使用小写字母和连字符
- 简洁、描述性强
- 示例: `code-review-expert`, `hello-world`
- 不允许: 空格、特殊字符、中文

**description** (必需)
- 清晰说明技能的使用场景
- 包含触发条件
- 详细但不冗长（50-200字）
- 示例格式：
  ```
  用于[功能]。当用户需要[场景1]、[场景2]或[场景3]时使用此技能。
  ```

**license** (推荐)
- 推荐使用 `MIT` 或 `Apache-2.0`
- 确保与项目整体许可证一致

### 2. 主体内容（必需）

#### 快速开始部分

```markdown
## 快速开始

当用户请求[功能]时，按以下流程执行：

1. **步骤一**: 描述
2. **步骤二**: 描述
3. **步骤三**: 描述
```

#### 使用示例

```markdown
### 基本使用

用户输入:
```
用户指令示例
```

Claude回应:
```
预期的回应示例
```
```

#### 技术栈映射（如适用）

```markdown
## 技术栈映射

根据代码类型，加载相应的专家指南：

| 技术栈 | 专家指南 | 触发条件 |
|--------|----------|----------|
| React | references/react.md | 检测到.jsx/.tsx文件 |
| Python | references/python.md | 检测到.py文件 |
```

### 3. 内容组织原则

#### 渐进式披露

**核心原则**：信息按需加载，避免一次性加载过多内容

1. **SKILL.md** - 核心工作流程和导航（<5k字）
2. **references/** - 详细参考资料，按需加载
3. **scripts/** - 可执行代码，无需读取即可执行

#### 内容分层

```
SKILL.md (快速流程)
  ├── references/topic1.md (详细指南)
  ├── references/topic2.md (详细指南)
  └── scripts/tool.py (执行工具)
```

---

## 文件命名规范

### 技能包命名

```
skill-name/           # 小写 + 连字符
├── SKILL.md
├── README.md
└── CHANGELOG.md
```

### 参考文件命名

```
references/
├── python.md         # 专题名称，小写
├── security.md
└── best-practices.md
```

### 脚本文件命名

```
scripts/
├── analyze.py        # 动词 + 名词
├── generate_report.py
└── helper.py
```

---

## 内容编写规范

### 1. 语言风格

- ✅ **使用中文** - 面向中文用户
- ✅ **专业术语** - 技术术语保留英文
- ✅ **简洁明了** - 避免冗余表达
- ✅ **结构清晰** - 使用标题、列表、表格

#### 示例

**❌ 不好的描述**:
```
这个技能是用来做代码审查的，可以从很多方面审查代码。
```

**✅ 好的描述**:
```
专业代码审查专家系统。提供全面深入的代码评审服务，涵盖前端、后端、Python、Java、Node.js等多个领域，
从代码质量、安全性、性能、架构设计、业务逻辑等多维度进行专业审查。
```

### 2. 代码示例

#### 格式要求

```markdown
**反模式**:
\`\`\`python
# ❌ 不好的做法
def bad_example():
    pass
\`\`\`

**最佳实践**:
\`\`\`python
# ✅ 好的做法
def good_example():
    pass
\`\`\`
```

#### 示例原则

- ✅ **可运行** - 代码示例应该可以运行
- ✅ **完整** - 包含必要的导入和上下文
- ✅ **注释** - 关键部分添加中文注释
- ✅ **对比** - 展示反模式和最佳实践对比

### 3. 列表和表格

#### 使用场景

- **列表** - 步骤、检查清单、要点
- **表格** - 对比、映射、配置

#### 示例

```markdown
### 审查清单
- [ ] 代码符合规范
- [ ] 错误处理完善
- [ ] 测试覆盖充分

### 技术栈对比
| 特性 | Option A | Option B |
|------|----------|----------|
| 性能 | 优秀 | 良好 |
| 易用性 | 中等 | 优秀 |
```

---

## 代码质量规范

### 1. 脚本代码规范

#### Python代码

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块功能描述
"""

import os
from pathlib import Path
from typing import List, Dict, Optional


def function_name(param1: str, param2: int) -> bool:
    """
    函数功能描述

    Args:
        param1: 参数1说明
        param2: 参数2说明

    Returns:
        返回值说明

    Raises:
        ValueError: 异常说明
    """
    # 实现逻辑
    pass


if __name__ == "__main__":
    # 主程序逻辑
    pass
```

#### 代码质量要求

- ✅ **类型注解** - 使用typing模块
- ✅ **文档字符串** - 每个函数都有docstring
- ✅ **错误处理** - 完善的异常处理
- ✅ **日志记录** - 适当的日志输出
- ✅ **可测试** - 易于单元测试

### 2. 性能考虑

- ⚠️ **避免阻塞** - 脚本执行时间应< 5秒
- ⚠️ **内存占用** - 避免加载大文件到内存
- ⚠️ **并发安全** - 考虑多线程/多进程场景

---

## 文档规范

### 1. README.md（必需）

每个技能包必须包含README.md：

```markdown
# Skill Name

简短描述（一句话）

## 功能特性

- 特性1
- 特性2

## 安装

安装步骤...

## 使用

使用示例...

## 配置

配置说明...

## 故障排除

常见问题...

## 参考资源

相关链接...
```

### 2. CHANGELOG.md（推荐）

```markdown
# Changelog

## [1.0.0] - 2025-12-26

### Added
- 新功能1
- 新功能2

### Changed
- 改进项1

### Fixed
- 修复问题1
```

### 3. 版本号规范

遵循 [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

示例: 1.2.3
- MAJOR: 不兼容的API更改
- MINOR: 向后兼容的功能新增
- PATCH: 向后兼容的问题修复
```

---

## 最佳实践

### 1. 技能设计原则

#### 单一职责

**✅ 好的做法**:
```
code-review-expert     # 仅专注于代码审查
pdf-generator          # 仅专注于PDF生成
```

**❌ 不好的做法**:
```
all-in-one-tool        # 功能太多，不够专注
utility-helper         # 名称模糊，用途不明确
```

#### 描述精确性

**✅ 好的description**:
```
用于代码审查和评审。当用户需要：(1) 代码质量评估, (2) 安全性审查,
(3) 架构设计评审, (4) 代码规范检查时使用此skill。
```

**❌ 不好的description**:
```
一个很有用的工具，可以帮你做很多事情。
```

### 2. 内容组织

#### 使用Progressive Disclosure

**SKILL.md** - 简洁流程（< 500行）
```markdown
# Quick Start
快速使用流程...

## For Details
- See [Python Guide](references/python.md) for Python-specific guidance
- See [Java Guide](references/java.md) for Java-specific guidance
```

**references/** - 详细指南
```markdown
# Python Review Guide

深入的内容可以放在这里，因为只有需要时才会加载。
```

### 3. 资源管理

#### scripts/ 目录

**用途**: 可执行的Python脚本

**何时包含**:
- ✅ 重复使用的代码逻辑
- ✅ 需要确定性的操作
- ✅ 跨平台的工具

**示例**:
```python
# scripts/git_helper.py
def get_git_info():
    """可重用的Git信息提取逻辑"""
    pass
```

#### references/ 目录

**用途**: 参考文档和详细指南

**何时包含**:
- ✅ 领域特定知识
- ✅ API文档
- ✅ 配置schema
- ✅ 详细的流程指南

**何时读取**:
- 仅在需要时由Claude加载
- 避免在SKILL.md中重复

#### assets/ 目录

**用途**: 输出中使用的文件（非代码）

**示例**:
- 模板文件
- 图片、图标
- 示例配置

**注意**:
- 不会加载到上下文
- 仅在生成输出时使用

### 4. 避免的内容

❌ **不要包含**:
- README.md（除了SKILL.md）
- INSTALL.md
- CONTRIBUTING.md
- 开发流程文档
- Changelog（除了CHANGELOG.md）

✅ **仅包含**:
- Claude执行工作所需的信息
- 技能运行所需的脚本和资源

---

## 提交审核清单

在提交技能包到市场前，请确保：

### 结构检查

- [ ] SKILL.md存在且格式正确
- [ ] README.md完整且清晰
- [ ] CHANGELOG.md包含版本信息
- [ ] 文件结构符合规范
- [ ] 所有文件使用UTF-8编码

### 内容检查

- [ ] description清晰明确，说明使用场景
- [ ] 使用示例完整可运行
- [ ] 代码示例有中文注释
- [ ] 技术术语使用正确
- [ ] 无错别字和语法错误

### 功能检查

- [ ] 技能包可以正常安装
- [ ] 在Claude Code中可以触发
- [ ] 执行结果符合预期
- [ ] 错误处理完善

### 代码质量检查

- [ ] Python代码有类型注解
- [ ] 函数有docstring
- [ ] 异常处理完善
- [ ] 无安全漏洞
- [ ] 性能合理（< 5秒）

### 文档检查

- [ ] README.md包含：
  - [ ] 功能描述
  - [ ] 安装说明
  - [ ] 使用示例
  - [ ] 配置说明
  - [ ] 故障排除

- [ ] CHANGELOG.md包含：
  - [ ] 版本号
  - [ ] 更新日期
  - [ ] 变更内容

### 兼容性检查

- [ ] 跨平台兼容（Windows/Linux/macOS）
- [ ] Python 3.6+ 兼容
- [ ] 依赖项明确列出

---

## 常见问题

### Q1: SKILL.md太长怎么办？

**A**: 使用Progressive Disclosure原则：
- 核心流程保留在SKILL.md
- 详细内容移到references/
- 脚本代码放到scripts/

### Q2: 如何处理多个技术栈？

**A**: 在SKILL.md中添加映射表：

```markdown
## 技术栈映射

| 技术栈 | 参考文件 | 触发条件 |
|--------|---------|---------|
| Python | references/python.md | 检测到.py文件 |
| Java | references/java.md | 检测到.java文件 |
```

### Q3: 脚本需要依赖库怎么办？

**A**: 在README.md中明确说明：

```markdown
## 依赖

- Python 3.6+
- requests库

## 安装

```bash
pip install requests
```
```

### Q4: 如何测试技能包？

**A**: 测试流程：
1. 安装到本地Claude skills目录
2. 重启Claude Code
3. 测试触发条件
4. 验证执行结果

---

## 参考资源

- [Claude Code Skills文档](https://docs.claudecode.com/skills)
- [Markdown写作规范](https://guides.github.com/features/mastering-markdown/)
- [Semantic Versioning](https://semver.org/)
- [Python代码风格指南](https://pep8.org/)

---

**版本**: 1.0.0
**更新日期**: 2025-12-26
**维护者**: Sino Claude Code Skills Marketplace Team
