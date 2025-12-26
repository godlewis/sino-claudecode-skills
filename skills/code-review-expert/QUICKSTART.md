# 快速开始指南

## 1️⃣ 基本使用

### 使用Claude进行代码审查

最简单的方式,直接告诉Claude:

```
请审查我的代码变更
```

或

```
对当前项目进行全面的代码审查
```

### 指定审查重点

```
请从安全性和性能角度审查我的代码
```

```
重点审查业务逻辑的正确性
```

### 指定技术栈

```
请审查我的React前端代码
```

```
帮我审查Python后端API
```

## 2️⃣ 使用Git信息提取工具

### 提取当前代码变更信息

```bash
# 获取当前状态的git信息
python scripts/get_git_info.py

# 输出示例:
# ================================================================================
# Git 仓库信息
# ================================================================================
# 【基本信息】
# 分支: feature/user-auth
# ...
```

### 指定提交范围

```bash
# 审查最近5次提交
python scripts/get_git_info.py --commit-range HEAD~5..HEAD

# 审查特定分支
python scripts/get_git_info.py --branch develop
```

### 导出为JSON格式

```bash
# 保存为JSON,方便后续处理
python scripts/get_git_info.py --format json > git_info.json

# 或直接输出
python scripts/get_git_info.py --format json
```

## 3️⃣ 生成代码审查报告

### 方法1: 使用辅助脚本

```bash
# 查看现有报告
python scripts/save_review_report.py --list

# 从文件生成报告
python scripts/save_review_report.py --input my_report.md

# 使用自定义名称
python scripts/save_review_report.py --input my_report.md --name "用户认证模块审查.md"
```

### 方法2: 在Python代码中使用

```python
from pathlib import Path
from scripts.save_review_report import save_report

# 读取或生成报告内容
report_content = """
# 代码审查报告

**审查日期**: 2025-12-26
**审查人员**: Claude Code Reviewer

## 审查结果
...

## 建议
...
"""

# 保存报告(自动使用中文文件名,自动创建docs目录)
report_path = save_report(report_content)
print(f"报告已保存: {report_path}")
```

### 方法3: 直接使用Claude生成

直接告诉Claude:

```
请生成代码审查报告并保存到docs目录
```

Claude会自动:
1. 提取git信息
2. 执行代码审查
3. 生成标准格式报告
4. 保存到 docs/代码审查报告_YYYY年MM月DD日HH时MM分.md

## 4️⃣ 完整工作流程示例

### 场景: 审查新功能的代码

```bash
# 1. 切换到功能分支
git checkout feature/new-feature

# 2. 提取变更信息
python scripts/get_git_info.py > git_info.txt

# 3. 让Claude进行审查
# (在Claude对话中)
# 请审查以下代码变更:
# [粘贴git_info.txt的内容]

# 4. Claude自动生成报告并保存到docs目录
```

### 场景: 定期代码审查

```bash
# 每周审查一次团队提交
python scripts/get_git_info.py --commit-range HEAD~20..HEAD > weekly_review.txt

# 让Claude审查
# 请对本周的代码变更(HEAD~20..HEAD)进行全面审查
```

## 5️⃣ 报告文件位置

### 默认位置

```
项目根目录/
└── docs/
    ├── 代码审查报告_2025年12月26日10时15分.md
    ├── 代码审查报告_2025年12月26日14时30分.md
    └── ...
```

### 查看所有报告

```bash
# 方法1: 使用脚本
python scripts/save_review_report.py --list

# 方法2: 直接查看
ls -lh docs/代码审查报告_*.md

# 方法3: 使用find
find docs -name "代码审查报告_*.md" -type f
```

## 6️⃣ 自定义和配置

### 修改报告命名格式

在 `scripts/save_review_report.py` 中的 `generate_report_filename()` 函数:

```python
def generate_report_filename() -> str:
    """生成报告文件名"""
    # 默认: 代码审查报告_2025年12月26日14时30分.md
    timestamp = datetime.now().strftime("%Y年%m月%d日%H时%M分")
    return f"代码审查报告_{timestamp}.md"

    # 或使用其他格式:
    # return f"CR_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    # return f"审查报告_{datetime.now().strftime('%Y-%m-%d')}.md"
```

### 修改docs目录名称

如果您的项目使用其他文档目录:

```python
def get_docs_directory() -> Path:
    """获取项目的文档目录"""
    project_root = Path.cwd()

    # 修改为您的目录名称
    doc_dirs = ["docs", "doc", "documentation", "reports"]

    for dir_name in doc_dirs:
        docs_dir = project_root / dir_name
        if docs_dir.exists() and docs_dir.is_dir():
            return docs_dir

    # 创建默认目录
    default_dir = project_root / "docs"
    default_dir.mkdir(parents=True, exist_ok=True)
    return default_dir
```

## 7️⃣ 集成到CI/CD

### GitHub Actions 示例

```yaml
name: Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  code-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Extract Git Info
        run: |
          python .claude/skills/code-review-expert/scripts/get_git_info.py \
            --format json \
            --output git_info.json

      - name: Generate Review Report
        run: |
          # 这里调用Claude API或使用其他方式生成报告
          python scripts/generate_review.py

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: code-review-report
          path: docs/代码审查报告_*.md
```

## 8️⃣ 常见问题

### Q1: 如何修改报告模板?

A: 编辑 `assets/review_report_template.md` 文件,使用占位符语法:
```markdown
{{PROJECT_NAME}}
{{REVIEW_DATE}}
{{DEVELOPER_NAME}}
```

### Q2: docs目录已存在但报告没有保存到那里?

A: 检查当前工作目录:
```bash
pwd  # 应该在项目根目录
```

### Q3: 如何批量重命名旧报告?

A: 使用脚本:
```bash
cd docs
for file in code_review_*.md; do
    new_name=$(echo $file | sed 's/code_review_\([0-9]\{8\}\)_\([0-9]\{6\}\)/代码审查报告_\1年\2月/g')
    mv "$file" "$new_name"
done
```

### Q4: 报告文件名支持开发者和分支信息吗?

A: 当前版本使用简化的命名(仅时间戳)。如需更多元数据,可以:
1. 在报告内容中包含这些信息
2. 修改 `generate_report_filename()` 函数添加更多字段

## 9️⃣ 进阶技巧

### 与Git钩子集成

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "执行代码审查..."

# 提取暂存区的变更
git diff --cached --name-status

# 可以在这里集成自动审查逻辑
# python scripts/get_git_info.py --commit-range HEAD~1..HEAD
```

### 自动发送报告

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_report(report_path: str, recipients: list):
    """发送代码审查报告邮件"""
    # 读取报告内容
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 创建邮件
    msg = MIMEMultipart()
    msg['Subject'] = f'代码审查报告 - {Path(report_path).stem}'
    msg['To'] = ', '.join(recipients)

    # 添加正文
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    # 发送邮件
    # ... SMTP配置
```

## 🔟 下一步

- 📖 阅读完整的 [README.md](README.md)
- 📝 查看更新日志 [CHANGELOG.md](CHANGELOG.md)
- 🎓 学习各领域专家指南 [references/](references/)
- 🔧 自定义报告模板 [assets/review_report_template.md](assets/review_report_template.md)

---

**提示**: 遇到问题? 查看 README.md 或运行:
```bash
python scripts/save_review_report.py --help
```
