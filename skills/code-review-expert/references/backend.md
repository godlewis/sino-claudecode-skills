# Backend Review Expert - 后端审查专家

## 审查范围

专注于后端代码质量、API设计、数据库交互、性能优化、错误处理、并发处理和服务可靠性。涵盖通用后端最佳实践。

## 核心审查维度

### 1. API设计

#### RESTful规范
**问题**: API设计不符合RESTful原则
**风险等级**: 中

**反模式**:
```python
# ❌ 不规范的API
@app.get('/getUsers')
@app.post('/createUser')
@app.post('/user/delete')
```

**最佳实践**:
```python
# ✅ RESTful API
@app.get('/users')           # 获取用户列表
@app.get('/users/{id}')      # 获取单个用户
@app.post('/users')          # 创建用户
@app.put('/users/{id}')      # 更新用户
@app.patch('/users/{id}')    # 部分更新
@app.delete('/users/{id}')   # 删除用户
```

**审查要点**:
- 使用正确的HTTP方法(GET/POST/PUT/PATCH/DELETE)
- URL使用名词复数形式(`/users`而非`/user`)
- 使用层级关系表达资源嵌套(`/users/{id}/posts`)
- 过滤、排序、分页使用查询参数

#### 响应格式一致性
**问题**: API响应格式不统一
**风险等级**: 中

**最佳实践**:
```json
// ✅ 统一的响应格式
{
  "data": { /* 实际数据 */ },
  "meta": {
    "page": 1,
    "perPage": 20,
    "total": 100
  },
  "errors": null
}

// 错误响应
{
  "data": null,
  "errors": [{
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "field": "email"
  }]
}
```

#### API版本控制
**问题**: 缺少API版本控制
**风险等级**: 中

**最佳实践**:
```python
# ✅ URL版本控制
@app.get('/api/v1/users')
@app.get('/api/v2/users')

# ✅ Header版本控制
# GET /api/users
# Accept: application/vnd.myapi.v2+json
```

### 2. 错误处理

#### HTTP状态码使用
**问题**: 使用错误的状态码
**风险等级**: 中

**最佳实践**:
```python
# ✅ 正确的状态码
# 200 OK - 成功
# 201 Created - 创建成功
# 204 No Content - 成功但无返回内容
# 400 Bad Request - 客户端请求错误
# 401 Unauthorized - 未认证
# 403 Forbidden - 无权限
# 404 Not Found - 资源不存在
# 409 Conflict - 资源冲突
# 422 Unprocessable Entity - 验证失败
# 429 Too Many Requests - 超过速率限制
# 500 Internal Server Error - 服务器错误
# 503 Service Unavailable - 服务不可用

@app.get('/users/{id}')
async def get_user(id: int):
    user = db.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

#### 异常处理链
**问题**: 吞掉异常或记录不充分
**风险等级**: 高

**反模式**:
```python
# ❌ 吞掉异常
try:
    process_data()
except:
    pass

# ❌ 捕获过于宽泛
try:
    process_data()
except Exception:
    pass
```

**最佳实践**:
```python
# ✅ 具体异常处理
try:
    process_data()
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
    raise HTTPException(status_code=422, detail=str(e))
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Internal error")
```

### 3. 数据验证

#### 输入验证
**问题**: 缺少输入验证或验证不充分
**风险等级**: 高

**最佳实践**:
```python
# ✅ 使用Pydantic进行验证
from pydantic import BaseModel, Field, EmailStr, validator

class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=18, le=120)
    password: str = Field(..., min_length=8)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('must be alphanumeric')
        return v

@app.post('/users')
async def create_user(request: CreateUserRequest):
    # 验证自动完成
    user = db.create_user(request.dict())
    return user
```

**审查要点**:
- 验证数据类型、长度、格式
- 验证业务规则(如年龄必须>=18)
- 验证枚举值
- 验证依赖关系(如password和password_confirm匹配)

### 4. 数据库交互

#### N+1查询问题
**问题**: N+1查询导致性能问题
**风险等级**: 高

**反模式**:
```python
# ❌ N+1查询
users = db.query('SELECT * FROM users')
for user in users:
    posts = db.query('SELECT * FROM posts WHERE user_id = ?', user.id)
    # 每个用户一次查询,共N+1次
```

**最佳实践**:
```python
# ✅ 使用JOIN或预加载
users = db.query('''
    SELECT u.*, p.*
    FROM users u
    LEFT JOIN posts p ON u.id = p.user_id
''')

# 或使用ORM的预加载
users = User.query.options(joinedload(User.posts)).all()
```

#### 事务管理
**问题**: 缺少事务或事务范围过大
**风险等级**: 高

**反模式**:
```python
# ❌ 缺少事务
def transfer_money(from_account, to_account, amount):
    db.update(from_account, balance=-amount)
    # 如果这里失败,数据不一致
    db.update(to_account, balance=amount)
```

**最佳实践**:
```python
# ✅ 使用事务
@transaction
def transfer_money(from_account, to_account, amount):
    try:
        db.update(from_account, balance=-amount)
        db.update(to_account, balance=amount)
        transaction.commit()
    except Exception:
        transaction.rollback()
        raise
```

#### 连接池管理
**问题**: 未正确管理数据库连接
**风险等级**: 高

**最佳实践**:
```python
# ✅ 使用连接池
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://...',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600
)
```

### 5. 性能优化

#### 缓存策略
**问题**: 缺少缓存或缓存策略不当
**风险等级**: 中

**最佳实践**:
```python
# ✅ Redis缓存
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379)

def cache_result(expiration=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_result(expiration=600)
async def get_user_stats(user_id: int):
    # 数据库查询
    pass
```

**审查要点**:
- 频繁访问但不常变化的数据应该缓存
- 缓存失效策略是否合理
- 缓存穿透、缓存雪崩防护

#### 分页
**问题**: 未分页或分页实现不当
**风险等级**: 高

**反模式**:
```python
# ❌ OFFSET在大数据集时性能差
@app.get('/users')
async def get_users(page: int = 1, per_page: int = 20):
    offset = (page - 1) * per_page
    # 当page=1000时,需要扫描1000*20行
    return db.query('SELECT * FROM users LIMIT ? OFFSET ?', per_page, offset)
```

**最佳实践**:
```python
# ✅ 使用游标分页
@app.get('/users')
async def get_users(last_id: int = None, limit: int = 20):
    if last_id:
        users = db.query(
            'SELECT * FROM users WHERE id > ? ORDER BY id LIMIT ?',
            last_id, limit
        )
    else:
        users = db.query('SELECT * FROM users ORDER BY id LIMIT ?', limit)
    return users
```

#### 批量操作
**问题**: 在循环中执行数据库操作
**风险等级**: 高

**反模式**:
```python
# ❌ 循环插入
for user_data in users_list:
    db.insert('users', user_data)  # N次数据库调用
```

**最佳实践**:
```python
# ✅ 批量插入
db.bulk_insert('users', users_list)  # 1次数据库调用

# 或使用executemany
db.executemany('INSERT INTO users VALUES (?, ?, ?)', users_list)
```

### 6. 并发和异步

#### 异步操作
**问题**: 混用同步和异步导致阻塞
**风险等级**: 高

**最佳实践**:
```python
# ✅ 正确使用async/await
import asyncio
import aiohttp

async def fetch_data(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_multiple_data(urls: List[str]):
    # 并发请求
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
```

#### 线程安全
**问题**: 共享状态未正确同步
**风险等级**: 高

**反模式**:
```python
# ❌ 非线程安全的共享状态
counter = 0

def increment():
    global counter
    counter += 1  # 竞态条件
```

**最佳实践**:
```python
# ✅ 使用锁
from threading import Lock

counter = 0
lock = Lock()

def increment():
    global counter
    with lock:
        counter += 1
```

### 7. 资源管理

#### 连接和资源释放
**问题**: 未正确释放资源
**风险等级**: 高

**反模式**:
```python
# ❌ 可能泄露连接
f = open('file.txt')
data = f.read()
# 如果异常,文件未关闭

conn = db.connect()
conn.query('SELECT * FROM users')
# 如果异常,连接未释放
```

**最佳实践**:
```python
# ✅ 使用上下文管理器
with open('file.txt') as f:
    data = f.read()
# 自动关闭

with db.connect() as conn:
    conn.query('SELECT * FROM users')
# 自动释放连接
```

#### 内存管理
**问题**: 加载大文件到内存
**风险等级**: 中

**最佳实践**:
```python
# ✅ 流式处理大文件
def process_large_file(filename):
    with open(filename) as f:
        for line in f:  # 逐行读取
            process_line(line)

# ✅ 分块上传/下载
def upload_large_file(file_path):
    chunk_size = 8192
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            upload_chunk(chunk)
```

### 8. 配置管理

#### 敏感信息
**问题**: 硬编码密钥和密码
**风险等级**: 严重

**反模式**:
```python
# ❌ 硬编码密钥
API_KEY = "sk_live_1234567890"
DB_PASSWORD = "admin123"
```

**最佳实践**:
```python
# ✅ 使用环境变量
import os

API_KEY = os.getenv('API_KEY')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# 或使用配置管理库
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    db_password: str

    class Config:
        env_file = '.env'

settings = Settings()
```

#### 配置分离
**问题**: 开发/生产配置混在一起
**风险等级**: 中

**最佳实践**:
```python
# ✅ 环境特定的配置
class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'postgres://prod'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'postgres://localhost/dev'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = os.getenv('DATABASE_URI')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}[os.getenv('ENV', 'development')]
```

### 9. 日志和监控

#### 结构化日志
**问题**: 日志格式不统一或缺少关键信息
**风险等级**: 中

**最佳实践**:
```python
# ✅ 结构化日志
import structlog

logger = structlog.get_logger()

logger.info(
    "user_login",
    user_id=user.id,
    ip_address=request.remote_addr,
    user_agent=request.headers.get('User-Agent'),
    timestamp=datetime.now().isoformat()
)

# 自动包含request_id用于追踪
logger = logger.bind(request_id=generate_request_id())
```

**审查要点**:
- 日志级别使用正确(ERROR/WARNING/INFO/DEBUG)
- 包含关键上下文信息(user_id, request_id等)
- 敏感信息已脱敏
- 结构化日志便于查询和分析

#### 健康检查
**问题**: 缺少健康检查端点
**风险等级**: 中

**最佳实践**:
```python
# ✅ 健康检查端点
@app.get('/health')
async def health_check():
    # 检查数据库连接
    db_status = await check_database()

    # 检查外部服务
    cache_status = await check_redis()

    status = 'healthy' if all([db_status, cache_status]) else 'unhealthy'

    return {
        'status': status,
        'timestamp': datetime.now().isoformat(),
        'checks': {
            'database': db_status,
            'cache': cache_status
        }
    }
```

## 性能指标

| 指标 | 目标 |
|------|------|
| API响应时间(P50) | < 200ms |
| API响应时间(P99) | < 1000ms |
| 错误率 | < 0.1% |
| 数据库查询时间 | < 100ms |
| 内存使用 | < 80% |
| CPU使用 | < 70% |

## 审查输出模板

```markdown
### [严重/高/中/低] 问题类型

**位置**: `文件路径:行号`

**问题描述**:
简明描述问题

**代码示例**:
\`\`\`python/java/etc
// ❌ 当前代码
有问题代码
\`\`\`

**改进建议**:
\`\`\`python/java/etc
// ✅ 建议代码
改进后代码
\`\`\`

**影响**:
- 性能: ...
- 可靠性: ...
- 可维护性: ...
```

## 工具推荐

- **性能分析**: cProfile, Py-Spy, New Relic, Datadog
- **API测试**: Postman, Insomnia, JMeter
- **数据库分析**: EXPLAIN query analysis
- **监控**: Prometheus, Grafana, ELK Stack

## 参考资源

- [Microsoft API Design Guide](https://github.com/microsoft/api-guidelines)
- [Zalando API Guidelines](https://github.com/zalando/restful-api-guidelines)
- [Google API Design Guide](https://cloud.google.com/apis/design)
- [12 Factor App](https://12factor.net/)
