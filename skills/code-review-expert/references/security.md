# Security Review Expert - 安全审查专家

## 审查范围

作为安全审查专家,专注于识别代码中的安全漏洞、风险和最佳实践违规。本指南适用于所有类型的代码审查。

## 核心安全问题检查清单

### 1. 注入攻击 (Injection)

#### SQL注入
**问题**: 未经充分验证的用户输入直接拼接到SQL查询中
**风险等级**: 严重

**反模式**:
```python
# ❌ 危险: 直接拼接SQL
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

**最佳实践**:
```python
# ✅ 安全: 使用参数化查询
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```

**审查要点**:
- 检查所有数据库查询是否使用参数化查询或ORM
- 搜索字符串拼接模式: `f"SELECT...{variable}"`
- 检查原生SQL执行点

#### 命令注入
**问题**: 用户输入未经清理直接用于系统命令
**风险等级**: 严重

**反模式**:
```python
# ❌ 危险
os.system(f"ping {user_input}")
subprocess.call(f"cat {filename}", shell=True)
```

**最佳实践**:
```python
# ✅ 安全: 使用参数化调用
subprocess.call(['ping', user_input])
subprocess.call(['cat', filename], shell=False)
```

#### NoSQL注入
**问题**: MongoDB等NoSQL查询中的注入攻击
**风险等级**: 严重

**反模式**:
```javascript
// ❌ 危险
db.users.find({ username: req.body.username, password: req.body.password });
```

**最佳实践**:
```javascript
// ✅ 安全: 使用类型检查和验证
const { username, password } = req.body;
if (typeof username !== 'string' || typeof password !== 'string') {
  throw new Error('Invalid input');
}
db.users.find({ username, password });
```

### 2. 跨站脚本攻击 (XSS)

**问题**: 未经转义的用户输入直接渲染到页面
**风险等级**: 严重

**反模式**:
```javascript
// ❌ 危险
element.innerHTML = userComment;
document.write(userContent);
```

**最佳实践**:
```javascript
// ✅ 安全: 使用textContent或DOMPurify
element.textContent = userComment;
// 或使用库进行清理
element.innerHTML = DOMPurify.sanitize(userComment);
```

**审查要点**:
- React/Vue/Angular中是否正确使用框架的安全机制
- 搜索 `dangerouslySetInnerHTML`, `v-html`, `[innerHTML]` 使用
- 检查用户生成内容(UGC)的渲染点

### 3. 认证和授权问题

#### 密码存储
**问题**: 明文或弱哈希存储密码
**风险等级**: 严重

**反模式**:
```python
# ❌ 危险
password = "plain_text_password"
db.save(username, password)

# ❌ 不安全: MD5/SHA1
hashed = md5(password)
```

**最佳实践**:
```python
# ✅ 安全: bcrypt/argon2
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

#### 会话管理
**问题**: 会话固定、会话劫持风险
**风险等级**: 高

**审查要点**:
- 登录后是否重新生成会话ID
- 会话超时是否合理
- 是否在HTTPS only标志下设置cookies
- 敏感操作是否需要重新认证

#### 权限检查
**问题**: 缺少权限验证或权限验证在客户端
**风险等级**: 严重

**反模式**:
```javascript
// ❌ 危险: 仅在客户端检查
if (user.role === 'admin') {
  // 前端显示管理员按钮
}
// 后端没有验证直接执行
app.delete('/api/users/:id', deleteUser); // 没有权限检查!
```

**最佳实践**:
```javascript
// ✅ 安全: 服务端验证
app.delete('/api/users/:id',
  authenticate,
  authorize(['admin']),  // 服务端权限检查
  deleteUser
);
```

### 4. 敏感数据暴露

#### 日志中的敏感信息
**问题**: 密码、token、PII等信息记录到日志
**风险等级**: 高

**反模式**:
```python
# ❌ 危险
logger.info(f"User login: {username}, {password}, {ssn}")
```

**最佳实践**:
```python
# ✅ 安全: 脱敏处理
logger.info(f"User login: {mask_username(username)}")
```

**审查要点**:
- 搜索所有日志语句
- 检查异常处理中的错误消息
- 验证调试模式是否关闭

#### 错误消息泄露
**问题**: 详细错误信息暴露内部实现
**风险等级**: 中

**反模式**:
```python
# ❌ 泄露数据库结构
except Exception as e:
    return {"error": str(e)}  # "Table 'users' doesn't exist..."
```

**最佳实践**:
```python
# ✅ 通用错误消息
except Exception as e:
    logger.error(e)  # 记录到日志
    return {"error": "Internal server error"}
```

### 5. 加密问题

#### HTTPS强制
**问题**: 未强制HTTPS,允许中间人攻击
**风险等级**: 高

**审查要点**:
- 检查cookie的 `secure` 标志
- 验证HTTP到HTTPS的重定向
- HSTS头是否设置

#### 随机数生成
**问题**: 使用可预测的随机数生成器
**风险等级**: 高

**反模式**:
```python
# ❌ 不安全
import random
token = random.random()  # 可预测
```

**最佳实践**:
```python
# ✅ 安全: 密码学安全的随机数
import secrets
token = secrets.token_urlsafe(32)
```

### 6. 业务逻辑安全

#### 价格/数量篡改
**问题**: 客户端可篡改关键业务参数
**风险等级**: 高

**反模式**:
```javascript
// ❌ 危险: 客户端计算价格
const total = items.reduce((sum, item) => sum + item.price, 0);
// 客户端发送total到服务器
```

**最佳实践**:
```javascript
// ✅ 安全: 服务端重新计算
const total = await calculateTotalServerSide(items);
if (clientTotal !== total) {
  throw new Error('Price mismatch');
}
```

#### 竞态条件
**问题**: 并发操作导致数据不一致
**风险等级**: 高

**反模式**:
```python
# ❌ 危险: 检查-使用竞态条件
if user.balance >= amount:
    # 在这里其他事务可能修改balance
    user.balance -= amount
```

**最佳实践**:
```python
# ✅ 安全: 原子操作或乐观锁
# 方法1: 数据库原子操作
UPDATE users SET balance = balance - ? WHERE id = ? AND balance >= ?

# 方法2: 乐观锁
updated = User.objects.filter(
    id=user_id,
    balance__gte=amount,
    version=current_version
).update(balance=F('balance') - amount, version=F('version') + 1)
```

### 7. 依赖安全

#### 已知漏洞的依赖
**问题**: 使用包含已知CVE的第三方库
**风险等级**: 严重

**审查要点**:
- 检查 `package.json`, `requirements.txt`, `pom.xml` 等
- 建议运行: `npm audit`, `pip check`, `snyk test`
- 检查是否有未维护的依赖

#### 版本固定
**问题**: 未锁定依赖版本导致意外更新
**风险等级**: 中

**最佳实践**:
- 使用 `package-lock.json`, `poetry.lock`
- 生产环境使用精确版本号

### 8. API安全

#### 速率限制
**问题**: 缺少API速率限制
**风险等级**: 高

**审查要点**:
- 公开API是否有速率限制
- 认证端点是否有暴力破解保护
- 是否有IP级别的限流

#### 输入验证
**问题**: 缺少输入类型、长度、格式验证
**风险等级**: 中

**最佳实践**:
```python
# ✅ 使用schema验证
from pydantic import BaseModel, Field

class UserInput(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr
    age: int = Field(..., ge=18, le=120)
```

## 审查输出模板

对每个发现的安全问题,按以下格式输出:

```markdown
### [严重/高/中/低] 安全问题类型

**位置**: `文件路径:行号`

**问题描述**:
简明描述安全问题

**代码示例**:
\`\`\`language
// ❌ 当前代码
有问题代码
\`\`\`

**改进建议**:
\`\`\`language
// ✅ 建议代码
修复后代码
\`\`\`

**风险**: 业务影响描述

**参考**: OWASP Top 10 / CWE-ID
```

## 优先级标准

- **严重 (Critical)**: 可被轻易利用的远程代码执行、数据泄露
- **高 (High)**: 需要一定条件但影响严重的安全问题
- **中 (Medium)**: 安全最佳实践违规,需要特定场景
- **低 (Low)**: 潜在的安全隐患,实际利用困难

## 工具推荐

- **静态分析**: SonarQube, CodeQL, Semgrep
- **依赖扫描**: npm audit, Snyk, Dependabot
- **SAST**: Bandit (Python), ESLint Security Plugin
- **DAST**: OWASP ZAP, Burp Suite

## 参考资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/archive/2023/2023_top25_list.html)
- [ASVS](https://owasp.org/www-project-application-security-verification-standard/)
