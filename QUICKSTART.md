# 快速开始指南

## 🎯 项目简介

**Sino Claude Code Skills Marketplace** 是中文Claude Code技能市场，提供高质量的技能包。

## 📦 安装技能包

### 方法1: 使用CLI工具（推荐）

```bash
# 查看所有可用技能包
python scripts/marketplace.py list

# 安装技能包
python scripts/marketplace.py install code-review-expert
```

### 方法2: 手动安装

```bash
# 复制技能包到Claude skills目录
cp -r skills/code-review-expert ~/.claude/skills/
```

## 🚀 使用技能包

安装后，在Claude Code中直接使用：

```
请审查我的代码
```

Claude会自动调用code-review-expert技能。

## 📊 项目结构

```
sino-claudecode-marketplace/
├── README.md                   # 项目说明
├── LICENSE                     # MIT许可证
├── .gitignore                  # Git忽略文件
├── scripts/                    # 工具脚本
│   └── marketplace.py         # 市场CLI工具
├── skills/                     # 技能包目录
│   ├── marketplace.json       # 市场配置
│   ├── code-review-expert/    # 代码审查专家
│   └── hello-world/           # 示例技能
├── docs/                       # 文档目录
└── examples/                   # 示例目录
```

## 🔧 CLI工具使用

```bash
# 列出所有技能包
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

# 查看统计信息
python scripts/marketplace.py stats
```

## 📚 技能包列表

### 🔍 代码质量

#### Code Review Expert ⭐
- **版本**: 1.1.0
- **功能**: 全面的代码审查
- **涵盖**: 安全/前端/后端/Python/Java/Node.js/架构/业务逻辑
- **特色**: Git信息提取、标准化报告、中文格式

### 🛠️ 开发工具

#### Hello World
- **版本**: 1.0.0
- **功能**: 示例模板
- **用途**: 学习和参考

## 🎓 贡献技能包

1. Fork项目
2. 创建技能包目录
3. 编写SKILL.md
4. 添加README.md
5. 更新marketplace.json
6. 提交Pull Request

## 📖 文档

- [完整README](README.md)
- [技能开发指南](docs/SKILL_DEVELOPMENT.md)
- [CLI使用说明](docs/CLI_USAGE.md)

## 🆘 常见问题

### Q: 如何安装技能包？
A: 使用 `python scripts/marketplace.py install <skill-id>`

### Q: 技能包保存在哪里？
A: `~/.claude/skills/`

### Q: 如何创建自己的技能包？
A: 参考 hello-world 示例，复制并修改

### Q: 安装后如何使用？
A: 在Claude Code中直接对话即可

## 📞 联系我们

- GitHub: https://github.com/godlewis/sino-claudecode-skills
- Issues: https://github.com/godlewis/sino-claudecode-skills/issues

---

**享受使用Claude Code Skills Marketplace！** 🎉
