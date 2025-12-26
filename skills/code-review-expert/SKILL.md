---
name: code-review-expert
description: 专业代码审查专家系统。提供全面深入的代码评审服务,涵盖前端、后端、Python、Java、Node.js等多个领域,从代码质量、安全性、性能、架构设计、业务逻辑等多维度进行专业审查。包含git提交信息提取和标准化的代码审查报告生成。当用户需要: (1) 代码审查和评审, (2) 代码质量评估, (3) 安全性审查, (4) 架构设计评审, (5) 代码规范检查, (6) 生成代码审查报告时使用此skill。
license: MIT
---

# Code Review Expert - 专业代码审查专家系统

## 快速开始

当用户请求代码审查时,按以下流程执行:

1. **获取变更信息** - 运行 `scripts/get_git_info.py` 获取git提交信息
2. **识别技术栈** - 分析代码文件,确定需要哪些领域的审查专家
3. **执行审查** - 根据技术栈加载相应的审查专家指南进行审查
4. **生成报告** - 使用 `assets/review_report_template.md` 模板生成标准化报告

## 技术栈与审查专家映射

根据代码类型和技术栈,加载对应的领域专家审查指南:

| 技术栈 | 审查专家指南 | 触发条件 |
|--------|------------|---------|
| 前端 (React/Vue/Angular/HTML/CSS/JS/TS) | `references/frontend.md` | 检测到 `.jsx`, `.tsx`, `.vue`, `.html`, `.css`, `.js`, `.ts` 文件 |
| 后端通用 | `references/backend.md` | 检测到服务器端代码 |
| Python | `references/python.md` | 检测到 `.py` 文件 |
| Java | `references/java.md` | 检测到 `.java` 文件 |
| Node.js | `references/nodejs.md` | 检测到 `package.json`, Node.js 服务器代码 |
| 安全审查 | `references/security.md` | 所有代码变更(始终包含) |
| 架构设计 | `references/architecture.md` | 涉及架构变更或设计模式 |
| 业务逻辑 | `references/business-logic.md` | 涉及核心业务流程或逻辑变更 |

**注意**: 安全审查 (`references/security.md`) 应该在所有代码审查中自动包含。

## 审查流程

### 第一步: 收集上下文信息

运行脚本获取git变更信息:

```bash
python scripts/get_git_info.py
```

该脚本会返回:
- 变更的文件列表
- Git diff 内容
- 提交者信息(姓名、邮箱)
- 提交时间和消息
- 分支信息

### 第二步: 识别代码变更范围

分析变更的文件,识别:
- 编程语言和技术栈
- 变更类型(新功能、Bug修复、重构、配置变更等)
- 影响范围(单个模块、跨模块、全系统等)

### 第三步: 加载并执行专家审查

根据识别的技术栈,加载相应的审查指南文件:

**示例场景**:
- 检测到React组件变更 → 加载 `references/frontend.md` 和 `references/security.md`
- 检测到Python API变更 → 加载 `references/python.md`, `references/backend.md`, `references/security.md`
- 检测到数据库schema变更 → 加载 `references/backend.md`, `references/architecture.md`, `references/business-logic.md`, `references/security.md`

每个专家指南文件包含:
- 该领域的核心审查要点
- 常见问题和反模式
- 最佳实践建议
- 具体的代码示例和改进建议

### 第四步: 综合审查结果

将各领域的审查结果综合整理,按优先级分类:

**严重问题 (Critical)** - 必须修复:
- 安全漏洞(SQL注入、XSS、权限绕过等)
- 数据泄露风险
- 资源泄露(内存、连接、文件句柄等)
- 严重的逻辑错误
- 并发安全问题

**警告 (Warning)** - 应该修复:
- 性能问题
- 可维护性问题
- 错误处理不当
- 代码重复
- 缺少必要的日志

**建议 (Suggestion)** - 建议改进:
- 代码风格和命名规范
- 文档注释完善
- 代码结构和组织
- 可读性改进
- 测试覆盖

### 第五步: 生成标准化报告

使用 `assets/review_report_template.md` 模板生成报告,并自动保存到 `docs/` 目录:

**Python实现代码**:
```python
import os
from datetime import datetime
from pathlib import Path

def generate_review_report(review_data: dict) -> str:
    """
    生成代码审查报告并保存到docs目录

    Args:
        review_data: 审查数据字典

    Returns:
        str: 保存的文件路径
    """
    # 1. 确定docs目录
    project_root = Path.cwd()
    docs_dir = project_root / "docs"

    # 如果docs不存在,检查doc是否存在
    if not docs_dir.exists():
        doc_dir = project_root / "doc"
        if doc_dir.exists():
            docs_dir = doc_dir
        else:
            # 创建docs目录
            docs_dir.mkdir(parents=True, exist_ok=True)

    # 2. 生成报告文件名(中文格式)
    timestamp = datetime.now().strftime("%Y年%m月%d日%H时%M分")
    report_filename = f"代码审查报告_{timestamp}.md"
    report_path = docs_dir / report_filename

    # 3. 读取模板文件
    template_path = Path(__file__).parent / "assets" / "review_report_template.md"
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # 4. 填充模板数据
    from string import Template
    template = Template(template_content)
    report_content = template.safe_substitute(**review_data)

    # 5. 保存报告
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"✅ 代码审查报告已生成: {report_path}")
    return str(report_path)

# 使用示例
if __name__ == "__main__":
    review_data = {
        "PROJECT_NAME": "MyProject",
        "REVIEW_DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "REVIEWER_NAME": "Claude Code Reviewer",
        "DEVELOPER_NAME": "张三",
        "DEVELOPER_EMAIL": "zhangsan@example.com",
        "BRANCH_NAME": "feature/user-auth",
        "COMMIT_HASH": "a1b2c3d",
        "COMMIT_MESSAGE": "feat: 添加用户认证功能",
        # ... 其他数据
    }

    report_path = generate_review_report(review_data)
```

报告包含以下部分:

1. **审查概览**
   - 项目名称
   - 审查日期和时间
   - 审查人员
   - Git分支和提交信息
   - 变更文件列表

2. **提交者信息**
   - 开发者姓名
   - 邮箱
   - 提交哈希
   - 提交消息

3. **变更摘要**
   - 变更类型
   - 影响范围
   - 涉及模块

4. **审查结果**
   - 按优先级分类的问题列表
   - 每个问题包含:
     - 问题描述
     - 严重程度
     - 所在文件和行号
     - 代码示例(当前代码 vs 建议代码)
     - 改进建议
     - 相关领域专家标识

5. **最佳实践建议**
   - 架构层面建议
   - 代码质量改进建议
   - 性能优化建议

6. **总体评分**
   - 代码质量评分(1-10分)
   - 安全性评分(1-10分)
   - 可维护性评分(1-10分)
   - 综合评分和评语

## 报告文件命名规范

生成的代码审查报告按以下格式命名:

```
代码审查报告_YYYY年MM月DD日HH时MM分.md
```

**示例**:
```
代码审查报告_2025年12月26日14时30分.md
```

命名规则:
- 前缀: `代码审查报告_`
- 时间戳: `YYYY年MM月DD日HH时MM分` (中文格式)
- 扩展名: `.md`

## 报告保存位置

代码审查报告自动保存到当前项目的 `docs/` 目录:

1. **优先使用** `docs/` 目录(项目根目录下的docs文件夹)
2. 如果 `docs/` 不存在，自动创建该目录
3. 完整路径示例: `项目根目录/docs/代码审查报告_2025年12月26日14时30分.md`

**目录检测逻辑**:
```bash
# 检查 docs 目录是否存在
if [ -d "docs" ]; then
    report_path="docs/代码审查报告_$(date +%Y年%m月%d日%H时%M分).md"
elif [ -d "doc" ]; then
    report_path="doc/代码审查报告_$(date +%Y年%m月%d日%H时%M分).md"
else
    # 创建 docs 目录
    mkdir -p docs
    report_path="docs/代码审查报告_$(date +%Y年%m月%d日%H时%M分).md"
fi
```

## 特殊场景处理

### 新功能开发
- 重点审查业务逻辑正确性
- 检查边界条件处理
- 验证错误处理完整性
- 评估扩展性设计

### Bug修复
- 验证根本原因是否解决
- 检查是否引入新问题
- 评估修复方案的完整性
- 建议添加回归测试

### 代码重构
- 评估重构后的代码质量
- 检查是否保持原有功能
- 验证性能是否改善
- 评估可维护性提升

### 紧急Hotfix
- 快速识别关键问题
- 优先关注安全性问题
- 简化报告格式
- 标记需要后续跟进的技术债务

## 审查原则

1. **建设性优先** - 提供具体可行的改进建议,而非仅指出问题
2. **尊重代码** - 尊重原作者的意图,理解上下文后再评判
3. **区分优先级** - 严重问题优先,避免因小失大
4. **结合上下文** - 考虑项目约束、时间压力、技术债务等因素
5. **持续改进** - 将审查作为学习和改进的机会,而非批评

## 工具使用

### Git信息提取
```bash
# 获取当前分支的变更信息
python scripts/get_git_info.py

# 指定提交范围
python scripts/get_git_info.py --commit-range HEAD~5..HEAD

# 指定分支
python scripts/get_git_info.py --branch feature/user-auth
```

### 多文件审查
对于大量文件变更,优先审查:
- 核心业务逻辑文件
- 安全敏感文件(认证、授权、数据处理)
- 架构关键文件
- 高风险文件(数据库操作、外部API调用)

## 质量保证

审查完成后,自检:
- [ ] 是否覆盖了所有变更的文件?
- [ ] 是否至少包含了安全审查?
- [ ] 是否识别了正确的技术栈并加载了相应的专家指南?
- [ ] 是否提供了具体的改进建议和代码示例?
- [ ] 是否按优先级对问题进行了分类?
- [ ] 是否生成了标准格式的报告?
- [ ] 报告命名是否符合规范?

## 扩展和定制

### 添加新的领域专家

在 `references/` 目录下创建新的审查指南文件,例如:
- `references/golang.md` - Go语言专家
- `references/rust.md` - Rust语言专家
- `references/mobile.md` - 移动端专家

更新SKILL.md中的技术栈映射表。

### 自定义审查模板

修改 `assets/review_report_template.md` 以适应团队或项目特定的报告格式需求。

### 扩展Git信息提取

修改 `scripts/get_git_info.py` 添加更多信息:
- JIRA/工单号
- 代码行数统计
- 复杂度分析
- 依赖关系图

## 相关参考

- [Google Code Review Guide](https://google.github.io/eng-practices/review/)
- [Clean Code by Robert C. Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [The Art of Readable Code](https://www.oreilly.com/library/view/the-art-of/9781449319283/)
