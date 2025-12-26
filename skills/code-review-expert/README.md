# Code Review Expert - 使用说明

## 📖 概述

Code Review Expert 是一个专业的代码审查技能,提供全面深入的代码评审服务。该技能涵盖前端、后端、Python、Java、Node.js等多个技术栈,从代码质量、安全性、性能、架构设计、业务逻辑等多维度进行专业审查。

## 🎯 核心功能

### 1. 多领域专家审查
- **安全审查专家** - 识别安全漏洞和风险
- **前端审查专家** - React/Vue/Angular等前端代码质量
- **后端审查专家** - API设计、数据库交互、性能优化
- **Python专家** - PEP 8、Pythonic风格、异步编程
- **Java专家** - JVM性能、并发、Spring框架
- **Node.js专家** - 异步编程、Express/Koa最佳实践
- **架构专家** - 设计模式、SOLID原则、可扩展性
- **业务逻辑专家** - 业务规则、流程完整性、数据一致性

### 2. Git信息提取
- 自动获取变更文件列表
- 提取提交者信息和提交历史
- 生成代码diff和统计信息
- 支持指定提交范围

### 3. 标准化审查报告
- 符合行业标准的审查报告格式
- 按优先级分类问题(严重/警告/建议)
- 提供具体代码示例和改进建议
- 多维度评分(质量/安全/性能/可维护性)

## 🚀 快速开始

### 基本使用

当您需要进行代码审查时,直接告知Claude:

```
请审查我的代码变更
```

或者:

```
对当前的git变更进行代码审查
```

### 高级用法

#### 1. 审查特定技术栈

```
请审查我的React前端代码
```

```
帮我审查这个Python后端API
```

#### 2. 指定审查重点

```
请重点审查安全性和性能问题
```

```
从架构设计的角度审查这段代码
```

#### 3. 审查指定范围的提交

```
请审查最近5次提交的代码
```

```
审查HEAD~10..HEAD范围的代码变更
```

## 📂 Skill结构

```
code-review-expert/
├── SKILL.md                           # 主技能文件
├── README.md                          # 使用说明
├── references/                        # 各领域审查专家指南
│   ├── security.md                   # 安全审查专家
│   ├── frontend.md                   # 前端审查专家
│   ├── backend.md                    # 后端审查专家
│   ├── python.md                     # Python专家
│   ├── java.md                       # Java专家
│   ├── nodejs.md                     # Node.js专家
│   ├── architecture.md               # 架构设计专家
│   └── business-logic.md             # 业务逻辑专家
├── scripts/
│   └── get_git_info.py              # Git信息提取工具
└── assets/
    └── review_report_template.md    # 审查报告模板
```

## 🛠️ Git信息提取工具

`get_git_info.py` 是一个独立的Python脚本,用于提取git仓库信息。

### 使用方法

```bash
# 获取当前状态信息
python scripts/get_git_info.py

# 获取指定提交范围的信息
python scripts/get_git_info.py --commit-range HEAD~5..HEAD

# 输出为JSON格式
python scripts/get_git_info.py --format json > git_info.json

# 保存到文件
python scripts/get_git_info.py --output review_data.txt
```

### 输出示例

**文本格式**:
```
================================================================================
Git 仓库信息
================================================================================

【基本信息】
分支: feature/user-auth
远程仓库: https://github.com/org/repo.git

【最后一次提交】
提交哈希: a1b2c3d
提交时间: 2025-12-26 14:30:22 +0800
作者: 张三 <zhangsan@example.com>
提交者: 张三 <zhangsan@example.com>
提交消息:
  feat: 添加用户认证功能

【变更文件列表】
  [M] src/auth/login.py - 已修改
  [A] src/auth/middleware.py - 新增
  [??] tests/test_auth.py - 未跟踪

【代码统计】
  变更文件数: 3
  新增行数: 245
  删除行数: 12
```

**JSON格式**:
```json
{
  "is_git_repo": true,
  "branch": "feature/user-auth",
  "remote_url": "https://github.com/org/repo.git",
  "last_commit": {
    "hash": "a1b2c3d4e5f6...",
    "short_hash": "a1b2c3d",
    "author": {
      "name": "张三",
      "email": "zhangsan@example.com"
    },
    "message": "feat: 添加用户认证功能"
  },
  "changed_files": [
    {
      "filename": "src/auth/login.py",
      "status": "M",
      "status_description": "已修改"
    }
  ],
  "statistics": {
    "files_changed": 3,
    "insertions": 245,
    "deletions": 12
  }
}
```

## 📊 审查报告

审查报告包含以下部分:

### 1. 审查概览
- 项目信息和提交信息
- 开发者和提交者信息
- 变更统计数据

### 2. 审查结果
按优先级分类的问题列表:
- **严重问题** (Critical) - 必须修复
- **警告** (Warning) - 应该修复
- **建议** (Suggestion) - 建议改进

每个问题包含:
- 问题描述和位置
- 当前代码和改进代码
- 审查专家标识
- 参考资源

### 3. 专项审查总结
- 安全性审查
- 前端/后端代码审查
- 业务逻辑审查
- 架构设计审查

### 4. 综合评分
- 代码质量
- 安全性
- 可维护性
- 性能
- 架构设计
- 业务逻辑

### 5. 审查结论
- 是否可以合并
- 后续行动项
- 责任人和截止日期

## 🎨 报告文件命名

代码审查报告按以下格式命名:

```
代码审查报告_YYYY年MM月DD日HH时MM分.md
```

**示例**:
```
代码审查报告_2025年12月26日14时30分.md
```

### 📁 报告保存位置

代码审查报告自动保存到当前项目的 `docs/` 目录:

- **优先使用** `docs/` 目录
- 如果 `docs/` 不存在，自动创建该目录
- 完整路径: `项目根目录/docs/代码审查报告_2025年12月26日14时30分.md`

## 📋 审查检查清单

代码审查会检查以下方面:

### 代码质量
- [ ] 代码符合项目规范
- [ ] 命名清晰易懂
- [ ] 函数/方法职责单一
- [ ] 代码复杂度合理
- [ ] 有适当的注释

### 安全性
- [ ] 无明显的安全漏洞
- [ ] 输入验证完善
- [ ] 敏感数据处理正确
- [ ] 权限检查到位

### 性能
- [ ] 无明显的性能问题
- [ ] 数据库查询优化
- [ ] 缓存策略合理
- [ ] 资源使用高效

### 可维护性
- [ ] 代码结构清晰
- [ ] 模块划分合理
- [ ] 依赖关系明确
- [ ] 易于扩展

### 测试
- [ ] 包含单元测试
- [ ] 测试覆盖率充分
- [ ] 测试用例合理
- [ ] 边界条件已测试

## 🔧 自定义和扩展

### 添加新的领域专家

1. 在 `references/` 目录下创建新的审查指南文件
   ```bash
   touch references/golang.md
   ```

2. 按照现有格式编写审查指南
   - 核心审查维度
   - 反模式和最佳实践
   - 审查要点
   - 工具推荐

3. 更新 `SKILL.md` 中的技术栈映射表

### 自定义审查模板

修改 `assets/review_report_template.md` 以适应团队或项目特定的报告格式需求。

### 扩展Git信息提取

修改 `scripts/get_git_info.py` 添加更多信息:
- JIRA/工单号
- 代码行数统计
- 复杂度分析
- 依赖关系图

## 📚 参考资源

- [Google Code Review Guide](https://google.github.io/eng-practices/review/)
- [Clean Code by Robert C. Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [The Art of Readable Code](https://www.oreilly.com/library/view/the-art-of/9781449319283/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [12 Factor App](https://12factor.net/)

## 💡 使用技巧

1. **明确审查重点**: 告诉Claude您关注的重点领域
2. **提供上下文**: 说明代码的业务背景和设计意图
3. **逐步审查**: 对于大型变更,可以分模块逐步审查
4. **结合CI/CD**: 将代码审查集成到CI/CD流程中
5. **团队协作**: 分享审查报告,促进团队学习

## 🤝 贡献

欢迎提出改进建议和最佳实践!

## 📄 许可证

MIT License

---

**版本**: 1.0.0
**更新日期**: 2025-12-26
**维护者**: Claude Code Review Expert Team
