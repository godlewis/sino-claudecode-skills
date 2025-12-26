# 🎯 Sino Claude Code Skills Marketplace

<div align="center">

**中文Claude Code技能市场**

提供高质量的专业技能包，提升您的Claude Code使用体验

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/Skills-1-blue.svg)](#)
[![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)](#)

</div>

---

## 📖 简介

**Sino Claude Code Skills Marketplace** 是一个专门为中文用户打造的Claude Code技能包市场，提供经过精心设计和测试的高质量技能包，帮助您更高效地使用Claude Code进行开发。

### ✨ 特性

- 🌏 **中文友好** - 专为中文用户设计，符合中文使用习惯
- 🎯 **专业质量** - 每个技能包都经过严格测试和优化
- 📦 **即装即用** - 简单的安装流程，快速上手
- 🔄 **持续更新** - 定期更新和维护，保持技能包最新
- 📚 **完善文档** - 详细的使用文档和示例
- 🛡️ **安全可靠** - 开源透明，可审计的代码

## 🚀 快速开始

### 安装技能包

#### 方法1: 使用CLI工具（推荐）

```bash
# 克隆市场仓库
git clone https://github.com/your-org/sino-claudecode-marketplace.git
cd sino-claudecode-marketplace

# 查看可用技能包
python scripts/marketplace.py list

# 安装技能包
python scripts/marketplace.py install code-review-expert
```

#### 方法2: 手动安装

```bash
# 1. 复制技能包到您的Claude skills目录
cp -r skills/code-review-expert ~/.claude/skills/

# 2. 重启Claude Code
# 技能包即可使用
```

### 使用技能包

安装完成后，在Claude Code中直接使用：

```
请审查我的代码变更
```

或

```
使用code-review-expert技能进行全面代码审查
```

## 📦 可用技能包

### 🔍 代码质量

#### [Code Review Expert](skills/code-review-expert/) ⭐ 推荐

**版本**: 1.1.0 | **下载量**: 0+ | **评分**: ⭐⭐⭐⭐⭐

全面专业的代码审查技能包，涵盖多个技术栈：

- 🛡️ **安全审查** - OWASP Top 10、常见漏洞识别
- 🎨 **前端审查** - React/Vue/Angular最佳实践
- ⚙️ **后端审查** - API设计、数据库优化
- 🐍 **Python专家** - PEP 8、异步编程
- ☕ **Java专家** - JVM、Spring框架
- 🟢 **Node.js专家** - 异步编程、Express/Koa
- 🏗️ **架构审查** - SOLID原则、设计模式
- 💼 **业务逻辑** - 业务规则验证、流程完整性

**特色功能**:
- Git信息自动提取
- 标准化审查报告生成
- 中文报告命名格式
- 自动保存到docs目录

[查看详情](skills/code-review-expert/README.md) | [更新日志](skills/code-review-expert/CHANGELOG.md)

---

### 🛠️ 开发工具

*更多技能包正在开发中...*

---

### 📝 文档编写

*更多技能包正在开发中...*

---

### 🧪 测试相关

*更多技能包正在开发中...*

---

### ⚡ 效率提升

*更多技能包正在开发中...*

## 📊 市场统计

| 指标 | 数值 |
|------|------|
| 📦 技能包总数 | 1 |
| 📂 分类数量 | 5 |
| 📥 总下载量 | 0 |
| 📅 最后更新 | 2025-12-26 |

## 🎯 贡献技能包

我们欢迎您贡献自己的技能包到市场！

### 贡献流程

1. **Fork项目**
   ```bash
   git clone https://github.com/your-username/sino-claudecode-marketplace.git
   ```

2. **创建技能包**
   ```bash
   mkdir skills/your-skill-name
   cd skills/your-skill-name
   # 创建SKILL.md和其他必需文件
   ```

3. **更新市场配置**
   ```json
   // 在skills/marketplace.json中添加您的技能包信息
   ```

4. **提交Pull Request**
   ```bash
   git add .
   git commit -m "Add new skill: your-skill-name"
   git push origin main
   ```

### 技能包要求

- ✅ 必须包含 `SKILL.md` 文件
- ✅ 必须有完整的 `README.md` 说明文档
- ✅ 遵循Skill结构规范
- ✅ 通过质量检查
- ✅ 有明确的使用场景和示例

## 🛠️ CLI工具

市场提供便捷的命令行工具：

```bash
# 查看所有可用技能包
python scripts/marketplace.py list

# 搜索技能包
python scripts/marketplace.py search code-review

# 查看技能包详情
python scripts/marketplace.py info code-review-expert

# 安装技能包
python scripts/marketplace.py install code-review-expert

# 卸载技能包
python scripts/marketplace.py uninstall code-review-expert

# 更新技能包
python scripts/marketplace.py update code-review-expert

# 更新市场索引
python scripts/marketplace.py update-market
```

## 📚 文档

- [快速开始指南](docs/QUICKSTART.md)
- [技能包开发指南](docs/SKILL_DEVELOPMENT.md)
- [CLI工具使用说明](docs/CLI_USAGE.md)
- [常见问题FAQ](docs/FAQ.md)

## 🤝 社区

- 💬 **讨论区**: [GitHub Discussions](https://github.com/your-org/sino-claudecode-marketplace/discussions)
- 🐛 **问题反馈**: [GitHub Issues](https://github.com/your-org/sino-claudecode-marketplace/issues)
- 💡 **功能建议**: [Feature Requests](https://github.com/your-org/sino-claudecode-marketplace/issues)
- 📧 **联系我们**: support@example.com

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

感谢所有为本项目贡献技能包和改进建议的开发者！

特别感谢：
- Claude Code团队提供的优秀工具
- 所有贡献者的辛勤付出
- 社区用户的宝贵反馈

---

<div align="center">

**[⬆ 返回顶部](#-sino-claude-code-skills-marketplace)**

Made with ❤️ by Claude Code Community

</div>
