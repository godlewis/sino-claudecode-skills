# 代码审查报告

**审查编号**: CR-{{TIMESTAMP}}-{{DEVELOPER_NAME}}
**审查日期**: {{REVIEW_DATE}}
**审查人员**: {{REVIEWER_NAME}}

---

## 📋 审查概览

| 项目 | 信息 |
|------|------|
| **项目名称** | {{PROJECT_NAME}} |
| **Git仓库** | {{REPOSITORY_URL}} |
| **Git分支** | {{BRANCH_NAME}} |
| **提交哈希** | `{{COMMIT_HASH}}` |
| **提交范围** | {{COMMIT_RANGE}} |

---

## 👤 提交者信息

| 属性 | 信息 |
|------|------|
| **开发者姓名** | {{DEVELOPER_NAME}} |
| **邮箱地址** | {{DEVELOPER_EMAIL}} |
| **提交者姓名** | {{COMMITTER_NAME}} |
| **提交者邮箱** | {{COMMITTER_EMAIL}} |
| **提交时间** | {{COMMIT_DATE}} |
| **提交消息** | {{COMMIT_MESSAGE}} |

---

## 📊 变更统计

| 指标 | 数值 |
|------|------|
| **变更文件数** | {{FILES_CHANGED}} |
| **新增行数** | {{INSERTIONS}} |
| **删除行数** | {{DELETIONS}} |
| **净增行数** | {{NET_CHANGES}} |

---

## 📁 变更文件列表

| 文件路径 | 状态 | 说明 |
|----------|------|------|
| {{FILE_1_PATH}} | {{FILE_1_STATUS}} | {{FILE_1_DESCRIPTION}} |
| {{FILE_2_PATH}} | {{FILE_2_STATUS}} | {{FILE_2_DESCRIPTION}} |

---

## 🔍 审查结果

### 严重问题 (Critical) - 必须修复

{{#if has_critical_issues}}

#### 1. [{{CRITICAL_ISSUE_1_CATEGORY}}] {{CRITICAL_ISSUE_1_TITLE}}

- **位置**: `{{CRITICAL_ISSUE_1_FILE}}:{{CRITICAL_ISSUE_1_LINE}}`
- **审查专家**: {{CRITICAL_ISSUE_1_EXPERT}}
- **问题描述**: {{CRITICAL_ISSUE_1_DESCRIPTION}}
- **风险**: {{CRITICAL_ISSUE_1_RISK}}

**当前代码**:
```{{CRITICAL_ISSUE_1_LANGUAGE}}
{{CRITICAL_ISSUE_1_CURRENT_CODE}}
```

**建议修复**:
```{{CRITICAL_ISSUE_1_LANGUAGE}}
{{CRITICAL_ISSUE_1_SUGGESTED_CODE}}
```

**参考**: {{CRITICAL_ISSUE_1_REFERENCE}}

---

{{/if}}

### 警告 (Warning) - 应该修复

{{#if has_warning_issues}}

#### 1. [{{WARNING_ISSUE_1_CATEGORY}}] {{WARNING_ISSUE_1_TITLE}}

- **位置**: `{{WARNING_ISSUE_1_FILE}}:{{WARNING_ISSUE_1_LINE}}`
- **审查专家**: {{WARNING_ISSUE_1_EXPERT}}
- **问题描述**: {{WARNING_ISSUE_1_DESCRIPTION}}
- **影响**: {{WARNING_ISSUE_1_IMPACT}}

**当前代码**:
```{{WARNING_ISSUE_1_LANGUAGE}}
{{WARNING_ISSUE_1_CURRENT_CODE}}
```

**建议改进**:
```{{WARNING_ISSUE_1_LANGUAGE}}
{{WARNING_ISSUE_1_SUGGESTED_CODE}}
```

---

{{/if}}

### 建议 (Suggestion) - 建议改进

{{#if has_suggestions}}

#### 1. [{{SUGGESTION_1_CATEGORY}}] {{SUGGESTION_1_TITLE}}

- **位置**: `{{SUGGESTION_1_FILE}}:{{SUGGESTION_1_LINE}}`
- **审查专家**: {{SUGGESTION_1_EXPERT}}
- **描述**: {{SUGGESTION_1_DESCRIPTION}}
- **收益**: {{SUGGESTION_1_BENEFIT}}

**当前实现**:
```{{SUGGESTION_1_LANGUAGE}}
{{SUGGESTION_1_CURRENT_CODE}}
```

**改进建议**:
```{{SUGGESTION_1_LANGUAGE}}
{{SUGGESTION_1_SUGGESTED_CODE}}
```

---

{{/if}}

---

## 💡 最佳实践建议

### 架构层面

{{#if has_architecture_suggestions}}

{{ARCHITECTURE_SUGGESTIONS}}

{{else}}

本次变更在架构层面表现良好,继续保持。

{{/if}}

### 代码质量

{{#if has_quality_suggestions}}

{{QUALITY_SUGGESTIONS}}

{{else}}

代码质量符合标准。

{{/if}}

### 性能优化

{{#if has_performance_suggestions}}

{{PERFORMANCE_SUGGESTIONS}}

{{else}}

未发现明显的性能问题。

{{/if}}

### 可维护性

{{#if has_maintainability_suggestions}}

{{MAINTAINABILITY_SUGGESTIONS}}

{{else}}

代码可维护性良好。

{{/if}}

---

## 🎯 专项审查总结

### 安全性审查

| 方面 | 状态 | 说明 |
|------|------|------|
| 注入攻击防护 | {{SECURITY_INJECTION_STATUS}} | {{SECURITY_INJECTION_DESC}} |
| 认证授权 | {{SECURITY_AUTH_STATUS}} | {{SECURITY_AUTH_DESC}} |
| 敏感数据处理 | {{SECURITY_DATA_STATUS}} | {{SECURITY_DATA_DESC}} |
| 加密与随机数 | {{SECURITY_CRYPTO_STATUS}} | {{SECURITY_CRYPTO_DESC}} |

**安全性评分**: {{SECURITY_SCORE}}/10 ⭐

---

### 前端审查 (如适用)

{{#if has_frontend_review}}

| 方面 | 状态 | 说明 |
|------|------|------|
| 组件设计 | {{FRONTEND_COMPONENT_STATUS}} | {{FRONTEND_COMPONENT_DESC}} |
| 状态管理 | {{FRONTEND_STATE_STATUS}} | {{FRONTEND_STATE_DESC}} |
| 性能优化 | {{FRONTEND_PERF_STATUS}} | {{FRONTEND_PERF_DESC}} |
| 可访问性 | {{FRONTEND_A11Y_STATUS}} | {{FRONTEND_A11Y_DESC}} |
| 代码风格 | {{FRONTEND_STYLE_STATUS}} | {{FRONTEND_STYLE_DESC}} |

**前端代码评分**: {{FRONTEND_SCORE}}/10 ⭐

{{/if}}

---

### 后端审查 (如适用)

{{#if has_backend_review}}

| 方面 | 状态 | 说明 |
|------|------|------|
| API设计 | {{BACKEND_API_STATUS}} | {{BACKEND_API_DESC}} |
| 错误处理 | {{BACKEND_ERROR_STATUS}} | {{BACKEND_ERROR_DESC}} |
| 数据验证 | {{BACKEND_VALIDATION_STATUS}} | {{BACKEND_VALIDATION_DESC}} |
| 数据库交互 | {{BACKEND_DB_STATUS}} | {{BACKEND_DB_DESC}} |
| 并发处理 | {{BACKEND_CONCURRENCY_STATUS}} | {{BACKEND_CONCURRENCY_DESC}} |

**后端代码评分**: {{BACKEND_SCORE}}/10 ⭐

{{/if}}

---

### 业务逻辑审查 (如适用)

{{#if has_business_logic_review}}

| 方面 | 状态 | 说明 |
|------|------|------|
| 业务规则验证 | {{BLOGIC_RULES_STATUS}} | {{BLOGIC_RULES_DESC}} |
| 边界条件处理 | {{BLOGIC_BOUNDARY_STATUS}} | {{BLOGIC_BOUNDARY_DESC}} |
| 数据一致性 | {{BLOGIC_CONSISTENCY_STATUS}} | {{BLOGIC_CONSISTENCY_DESC}} |
| 业务流程 | {{BLOGIC_FLOW_STATUS}} | {{BLOGIC_FLOW_DESC}} |
| 异常处理 | {{BLOGIC_EXCEPTION_STATUS}} | {{BLOGIC_EXCEPTION_DESC}} |

**业务逻辑评分**: {{BLOGIC_SCORE}}/10 ⭐

{{/if}}

---

### 架构设计审查 (如适用)

{{#if has_architecture_review}}

| 方面 | 状态 | 说明 |
|------|------|------|
| 模块划分 | {{ARCH_MODULE_STATUS}} | {{ARCH_MODULE_DESC}} |
| 依赖关系 | {{ARCH_DEPENDENCY_STATUS}} | {{ARCH_DEPENDENCY_DESC}} |
| 设计模式 | {{ARCH_PATTERN_STATUS}} | {{ARCH_PATTERN_DESC}} |
| 可扩展性 | {{ARCH_SCALABILITY_STATUS}} | {{ARCH_SCALABILITY_DESC}} |
| SOLID原则 | {{ARCH_SOLID_STATUS}} | {{ARCH_SOLID_DESC}} |

**架构设计评分**: {{ARCH_SCORE}}/10 ⭐

{{/if}}

---

## 📈 综合评分

| 维度 | 评分 | 说明 |
|------|------|------|
| **代码质量** | {{QUALITY_SCORE}}/10 | {{QUALITY_COMMENT}} |
| **安全性** | {{SECURITY_SCORE_OVERALL}}/10 | {{SECURITY_COMMENT}} |
| **可维护性** | {{MAINTAINABILITY_SCORE}}/10 | {{MAINTAINABILITY_COMMENT}} |
| **性能** | {{PERFORMANCE_SCORE}}/10 | {{PERFORMANCE_COMMENT}} |
| **架构设计** | {{ARCHITECTURE_SCORE}}/10 | {{ARCHITECTURE_COMMENT}} |
| **业务逻辑** | {{BUSINESS_LOGIC_SCORE}}/10 | {{BUSINESS_LOGIC_COMMENT}} |

### 总体评分: **{{OVERALL_SCORE}}/10** ⭐⭐⭐⭐⭐

**综合评价**:
{{OVERALL_COMMENT}}

---

## ✅ 审查检查清单

### 代码质量
- [x] 代码符合项目规范
- [ ] 命名清晰易懂
- [ ] 函数/方法职责单一
- [ ] 代码复杂度合理
- [ ] 有适当的注释

### 安全性
- [ ] 无明显的安全漏洞
- [ ] 输入验证完善
- [ ] 敏感数据处理正确
- [ ] 权限检查到位

### 测试
- [ ] 包含单元测试
- [ ] 测试覆盖率充分
- [ ] 测试用例合理
- [ ] 边界条件已测试

### 文档
- [ ] API文档更新
- [ ] README更新(如需要)
- [ ] 变更日志更新
- [ ] 技术文档完善

---

## 📝 审查结论

{{#if has_critical_issues}}

### ❌ 需要修改后合并

发现{{CRITICAL_COUNT}}个严重问题必须修复,请开发者在合并前完成以下修改:

1. {{CRITICAL_ACTION_1}}
2. {{CRITICAL_ACTION_2}}
3. {{CRITICAL_ACTION_3}}

修复后请重新提交代码审查。

{{else if has_warning_issues}}

### ⚠️ 建议修改后合并

发现{{WARNING_COUNT}}个警告问题,建议修复后再合并。但如果时间紧迫,可以:

- 立即修复必须的问题
- 创建技术债务票据跟踪其他问题
- 在后续迭代中解决

{{else}}

### ✅ 可以合并

代码质量良好,可以合并。感谢您的贡献!

{{/if}}

---

## 🔧 后续行动

| 优先级 | 行动项 | 责任人 | 截止日期 |
|--------|--------|--------|----------|
| 高 | {{ACTION_1}} | {{OWNER_1}} | {{DUE_DATE_1}} |
| 中 | {{ACTION_2}} | {{OWNER_2}} | {{DUE_DATE_2}} |
| 低 | {{ACTION_3}} | {{OWNER_3}} | {{DUE_DATE_3}} |

---

## 📚 参考资源

- 项目代码规范: {{PROJECT_CODING_STANDARDS_URL}}
- 安全最佳实践: {{SECURITY_BEST_PRACTICES_URL}}
- 架构文档: {{ARCHITECTURE_DOC_URL}}
- 开发者指南: {{DEVELOPER_GUIDE_URL}}

---

## 💬 审查者留言

{{REVIEWER_COMMENTS}}

---

**报告生成时间**: {{REPORT_GENERATED_AT}}
**报告版本**: 1.0
**审查工具**: Claude Code Review Expert

---

## 附录: 变更详情

### 文件变更详情

{{FILE_CHANGE_DETAILS}}

### Git Diff

```diff
{{GIT_DIFF}}
```
