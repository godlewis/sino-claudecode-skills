# Code Review Expert - 更新日志

## 版本 1.1.0 - 2025-12-26

### 🎉 新增功能

#### 1. 中文报告命名规范
- 报告文件名改为中文格式: `代码审查报告_YYYY年MM月DD日HH时MM分.md`
- 示例: `代码审查报告_2025年12月26日14时30分.md`
- 更符合中文用户习惯,易于识别和管理

#### 2. 自动保存到docs目录
- 报告自动保存到项目根目录的 `docs/` 文件夹
- 如果 `docs/` 不存在,则自动创建
- 支持 `doc/` 目录作为备选(如果已存在)

#### 3. 报告保存辅助脚本
新增 `scripts/save_review_report.py` 工具,提供:
- 自动创建docs目录
- 生成中文格式的报告文件名
- 支持从文件、标准输入或命令行参数读取内容
- 列出现有报告功能

### 📝 修改文件

1. **SKILL.md**
   - 更新报告命名规范说明
   - 添加完整的Python实现代码
   - 新增目录检测和创建逻辑
   - 添加实际使用示例

2. **README.md**
   - 更新报告命名规范章节
   - 添加报告保存位置说明
   - 更新使用示例

3. **scripts/save_review_report.py** (新增)
   - 完整的报告保存工具
   - 命令行参数支持
   - 列出现有报告功能

### 🔧 使用方法

#### 基本使用
```bash
# 查看现有报告
python scripts/save_review_report.py --list

# 从标准输入读取报告
cat report.md | python scripts/save_review_report.py

# 从文件读取报告
python scripts/save_review_report.py --input report.md

# 使用自定义文件名
python scripts/save_review_report.py --input report.md --name "用户认证模块审查.md"
```

#### Python代码集成
```python
from scripts.save_review_report import save_report, generate_report_filename

# 方法1: 直接保存
report_content = "# 代码审查报告\n\n这是审查内容..."
report_path = save_report(report_content)
print(f"报告已保存到: {report_path}")

# 方法2: 使用自定义文件名
report_path = save_report(report_content, custom_name="重要功能审查.md")

# 方法3: 列出现有报告
from scripts.save_review_report import list_existing_reports
reports = list_existing_reports()
for report in reports:
    print(f"{report.name} - {report.stat().st_size} 字节")
```

### 📋 报告文件路径示例

```
项目根目录/
├── docs/                           # 自动创建(如果不存在)
│   ├── 代码审查报告_2025年12月26日10时15分.md
│   ├── 代码审查报告_2025年12月26日14时30分.md
│   └── 代码审查报告_2025年12月26日16时45分.md
├── src/
├── tests/
└── README.md
```

### 🎯 核心改进

1. **更友好的命名**: 中文格式更符合国内团队习惯
2. **自动化**: 无需手动创建目录,自动处理
3. **标准化**: 统一的报告存储位置
4. **灵活性**: 支持自定义文件名和多种输入方式
5. **可追溯**: 列出命令可快速查看所有历史报告

### 📊 兼容性

- ✅ 向后兼容: 原有的代码审查逻辑完全保留
- ✅ 跨平台: Windows/Linux/macOS 完全支持
- ✅ Python 3.6+: 支持所有主流Python版本
- ✅ UTF-8编码: 完美支持中文内容

### 🔄 迁移指南

如果您之前使用旧版本,无需任何代码修改:

1. **旧版本报告** (如果有):
   - `code_review_20251226_143022_feature_xxx.md`
   - 仍然有效,无需重命名

2. **新生成的报告**:
   - 自动使用新的中文命名
   - 自动保存到 docs/ 目录

3. **可选操作**:
   ```bash
   # 如果需要统一格式,可以重命名旧报告
   mv code_review_*.md docs/
   ```

### 🐛 已知问题

暂无

### 📞 技术支持

如遇问题,请检查:
1. Python版本 >= 3.6
2. 对项目目录有写权限
3. 文件名编码为UTF-8

---

## 版本 1.0.0 - 2025-12-26

### 🎉 首次发布

- 创建Code Review Expert skill
- 8个领域专家审查指南
- Git信息提取工具
- 标准审查报告模板
- 完整的使用文档

---

**更新日期**: 2025-12-26
**维护者**: Claude Code Review Expert Team
