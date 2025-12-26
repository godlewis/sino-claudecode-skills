# Node.js Review Expert - Node.js代码审查专家

## 审查范围

专注于Node.js异步编程、事件循环、错误处理、Express/Koa框架最佳实践、包管理和性能优化。

## 核心审查维度

### 1. 异步编程

#### Promise使用
**问题**: 回调地狱或Promise使用不当
**风险等级**: 高

**反模式**:
```javascript
// ❌ 回调地狱
function getUserData(userId, callback) {
  getUser(userId, (err, user) => {
    if (err) return callback(err);
    getPosts(user.id, (err, posts) => {
      if (err) return callback(err);
      getComments(posts.map(p => p.id), (err, comments) => {
        if (err) return callback(err);
        callback(null, { user, posts, comments });
      });
    });
  });
}
```

**最佳实践**:
```javascript
// ✅ 使用async/await
async function getUserData(userId) {
  try {
    const user = await getUser(userId);
    const posts = await getPosts(user.id);
    const comments = await getComments(posts.map(p => p.id));
    return { user, posts, comments };
  } catch (error) {
    // 统一错误处理
    throw new UserDataError('Failed to fetch user data', error);
  }
}
```

#### 并发控制
**问题**: 串行执行可并行任务
**风险等级**: 中

**反模式**:
```javascript
// ❌ 串行执行独立任务
async function fetchAllData() {
  const users = await fetchUsers();
  const posts = await fetchPosts();
  const comments = await fetchComments();
  return { users, posts, comments };
}
```

**最佳实践**:
```javascript
// ✅ 并行执行独立任务
async function fetchAllData() {
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments()
  ]);
  return { users, posts, comments };
}

// ✅ 带并发限制
async function fetchAllDataWithLimit() {
  const tasks = [
    fetchUsers,
    fetchPosts,
    fetchComments,
    // ...更多任务
  ];

  const results = [];
  const limit = 3; // 最多3个并发

  for (let i = 0; i < tasks.length; i += limit) {
    const batch = tasks.slice(i, i + limit);
    const batchResults = await Promise.all(
      batch.map(task => task())
    );
    results.push(...batchResults);
  }

  return results;
}
```

### 2. 错误处理

#### 未捕获的Promise拒绝
**问题**: Promise拒绝未处理
**风险等级**: 高

**反模式**:
```javascript
// ❌ 未处理的Promise拒绝
function fetchData() {
  return fetch(url).then(res => res.json());
  // 如果fetch失败,拒绝未处理
}

// ❌ 空的catch
fetchData().catch(() => {});
```

**最佳实践**:
```javascript
// ✅ 正确处理错误
async function fetchData() {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    logger.error('Failed to fetch data:', error);
    throw error; // 重新抛出让调用者处理
  }
}

// ✅ 全局未处理拒绝处理
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // 根据需要决定是否退出进程
});

// ✅ 全局未捕获异常处理
process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception:', error);
  // 清理资源后退出
  process.exit(1);
});
```

#### Error对象使用
**问题**: 抛出字符串而非Error对象
**风险等级**: 中

**反模式**:
```javascript
// ❌ 抛出字符串
if (!user) {
  throw 'User not found';
}
```

**最佳实践**:
```javascript
// ✅ 抛出Error对象
if (!user) {
  throw new Error('User not found');
}

// ✅ 自定义Error类
class UserNotFoundError extends Error {
  constructor(userId) {
    super(`User with id ${userId} not found`);
    this.name = 'UserNotFoundError';
    this.userId = userId;
  }
}

throw new UserNotFoundError(userId);
```

### 3. Express/Koa最佳实践

#### 路由组织
**问题**: 所有路由定义在主文件中
**风险等级**: 中

**反模式**:
```javascript
// ❌ app.js包含所有路由
const express = require('express');
const app = express();

app.get('/users', (req, res) => { /* ... */ });
app.post('/users', (req, res) => { /* ... */ });
app.get('/users/:id', (req, res) => { /* ... */ });
// ...100+个路由
```

**最佳实践**:
```javascript
// ✅ 模块化路由
// routes/users.js
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');
const { validateUser } = require('../middleware/validation');

router.get('/', userController.getUsers);
router.post('/', validateUser, userController.createUser);
router.get('/:id', userController.getUserById);
router.put('/:id', validateUser, userController.updateUser);
router.delete('/:id', userController.deleteUser);

module.exports = router;

// app.js
const userRoutes = require('./routes/users');
app.use('/api/users', userRoutes);
```

#### 中间件错误处理
**问题**: 缺少错误处理中间件
**风险等级**: 高

**反模式**:
```javascript
// ❌ 缺少错误处理
app.get('/users/:id', async (req, res) => {
  const user = await db.findUser(req.params.id);
  res.json(user);
  // 如果db.findUser抛出异常,程序崩溃
});
```

**最佳实践**:
```javascript
// ✅ 错误处理中间件
// middleware/asyncHandler.js
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// 使用
app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await db.findUser(req.params.id);
  res.json(user);
}));

// ✅ 全局错误处理中间件
app.use((err, req, res, next) => {
  logger.error(err.stack);

  // 生产环境不暴露详细错误
  const isDevelopment = process.env.NODE_ENV === 'development';

  res.status(err.status || 500).json({
    error: {
      message: err.message || 'Internal Server Error',
      ...(isDevelopment && { stack: err.stack })
    }
  });
});
```

#### 请求验证
**问题**: 缺少输入验证
**风险等级**: 高

**最佳实践**:
```javascript
// ✅ 使用express-validator
const { body, param, validationResult } = require('express-validator');

app.post('/users',
  [
    body('username').isLength({ min: 3, max: 50 }).trim(),
    body('email').isEmail().normalizeEmail(),
    body('age').isInt({ min: 18, max: 120 })
  ],
  asyncHandler(async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const user = await createUser(req.body);
    res.status(201).json(user);
  })
);

// ✅ 使用Joi schema验证
const Joi = require('joi');

const userSchema = Joi.object({
  username: Joi.string().min(3).max(50).required(),
  email: Joi.string().email().required(),
  age: Joi.number().integer().min(18).max(120).required()
});

app.post('/users', asyncHandler(async (req, res) => {
  const { error, value } = userSchema.validate(req.body);
  if (error) {
    return res.status(400).json({ error: error.details[0].message });
  }

  const user = await createUser(value);
  res.status(201).json(user);
}));
```

### 4. 性能优化

#### 事件循环阻塞
**问题**: 同步操作阻塞事件循环
**风险等级**: 高

**反模式**:
```javascript
// ❌ 阻塞事件循环
app.get('/report', async (req, res) => {
  const data = fs.readFileSync('large-file.json');  // 同步读取
  const result = cpuIntensiveCalculation(data);    // CPU密集计算
  res.json(result);
});
```

**最佳实践**:
```javascript
// ✅ 使用异步操作
app.get('/report', asyncHandler(async (req, res) => {
  const data = await fs.promises.readFile('large-file.json');
  const result = await cpuIntensiveCalculationAsync(data);
  res.json(result);
}));

// ✅ CPU密集任务使用worker threads
const { Worker } = require('worker_threads');

app.get('/report', asyncHandler(async (req, res) => {
  const worker = new Worker('./heavy-computation.js', {
    workerData: req.body
  });

  worker.on('message', (result) => {
    res.json(result);
  });

  worker.on('error', (error) => {
    next(error);
  });
}));
```

#### 内存泄漏
**问题**: 全局变量累积、闭包持有引用
**风险等级**: 高

**反模式**:
```javascript
// ❌ 全局变量累积
const cache = {};  // 永远增长

app.get('/data', (req, res) => {
  const key = req.params.id;
  cache[key] = fetchData();  // 无限增长
  res.json(cache[key]);
});
```

**最佳实践**:
```javascript
// ✅ 使用LRU缓存
const LRU = require('lru-cache');

const cache = new LRU({
  max: 500,        // 最多500项
  ttl: 1000 * 60 * 5,  // 5分钟过期
});

app.get('/data', (req, res) => {
  const key = req.params.id;
  let data = cache.get(key);

  if (!data) {
    data = fetchData();
    cache.set(key, data);
  }

  res.json(data);
});

// ✅ 使用Redis作为分布式缓存
const redis = require('redis');
const client = redis.createClient();

app.get('/data', asyncHandler(async (req, res) => {
  const key = req.params.id;
  let data = await client.get(key);

  if (!data) {
    data = await fetchData();
    await client.setEx(key, 300, JSON.stringify(data));  // 5分钟
  } else {
    data = JSON.parse(data);
  }

  res.json(data);
}));
```

#### 流式处理
**问题**: 大文件一次性加载到内存
**风险等级**: 高

**反模式**:
```javascript
// ❌ 一次性加载大文件
app.get('/download', (req, res) => {
  const file = fs.readFileSync('large-file.zip');  // 耗尽内存
  res.send(file);
});
```

**最佳实践**:
```javascript
// ✅ 使用流
app.get('/download', (req, res) => {
  const stream = fs.createReadStream('large-file.zip');
  stream.pipe(res);
});

// ✅ 处理上传
app.post('/upload', (req, res) => {
  const stream = fs.createWriteStream('upload.bin');
  req.pipe(stream);

  stream.on('finish', () => {
    res.status(200).send('Upload complete');
  });

  stream.on('error', (error) => {
    res.status(500).send('Upload failed');
  });
});
```

### 5. 安全性

#### 敏感数据
**问题**: 硬编码密钥或暴露敏感信息
**风险等级**: 严重

**反模式**:
```javascript
// ❌ 硬编码密钥
const API_KEY = 'sk_live_1234567890abcdef';
const DB_PASSWORD = 'admin123';

// ❌ 暴露堆栈信息
app.use((err, req, res, next) => {
  res.status(500).json({
    error: err.message,
    stack: err.stack  // 暴露内部实现
  });
});
```

**最佳实践**:
```javascript
// ✅ 使用环境变量
require('dotenv').config();

const API_KEY = process.env.API_KEY;
const DB_PASSWORD = process.env.DB_PASSWORD;

// ✅ 生产环境不暴露堆栈
app.use((err, req, res, next) => {
  const isDevelopment = process.env.NODE_ENV === 'development';

  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error',
    ...(isDevelopment && { stack: err.stack })
  });
});
```

#### Helmet安全头
**问题**: 缺少安全HTTP头
**风险等级**: 中

**最佳实践**:
```javascript
// ✅ 使用Helmet
const helmet = require('helmet');

app.use(helmet());

// 或自定义配置
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
```

### 6. 包管理

#### 依赖版本
**问题**: 依赖版本未锁定
**风险等级**: 高

**最佳实践**:
```bash
# ✅ 使用package-lock.json
npm install

# ✅ 使用精确版本
{
  "dependencies": {
    "express": "4.18.2",      // 精确版本
    "mongoose": "^7.0.0"      // 允许小版本更新
  }
}

# ✅ 使用npm ci进行生产安装
npm ci  # 而不是npm install
```

#### 依赖审计
**问题**: 未检查依赖漏洞
**风险等级**: 高

```bash
# ✅ 定期运行审计
npm audit
npm audit fix

# ✅ 使用npm-force-resolutions解决传递依赖问题
{
  "scripts": {
    "preinstall": "npx npm-force-resolutions"
  },
  "resolutions": {
    "lodash": "^4.17.21",
    "minimist": "^1.2.6"
  }
}
```

### 7. 日志和监控

#### 结构化日志
**问题**: 日志格式不统一
**风险等级**: 中

**反模式**:
```javascript
// ❌ 随意console.log
console.log('User logged in');
console.error('Error:', error);
console.log('Data:', JSON.stringify(data));
```

**最佳实践**:
```javascript
// ✅ 使用Winston结构化日志
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}

// 使用
logger.info('User logged in', {
  userId: user.id,
  ip: req.ip,
  userAgent: req.get('user-agent'),
  timestamp: new Date().toISOString()
});

logger.error('Database error', {
  error: error.message,
  stack: error.stack,
  query: query.sql
});
```

#### 健康检查
**问题**: 缺少健康检查端点
**风险等级**: 中

**最佳实践**:
```javascript
// ✅ 健康检查端点
app.get('/health', async (req, res) => {
  const health = {
    uptime: process.uptime(),
    timestamp: Date.now(),
    checks: {
      database: 'unknown',
      redis: 'unknown'
    }
  };

  try {
    await db.ping();
    health.checks.database = 'healthy';
  } catch (error) {
    health.checks.database = 'unhealthy';
  }

  try {
    await redis.ping();
    health.checks.redis = 'healthy';
  } catch (error) {
    health.checks.redis = 'unhealthy';
  }

  const isHealthy = Object.values(health.checks)
    .every(status => status === 'healthy');

  res.status(isHealthy ? 200 : 503).json(health);
});
```

### 8. TypeScript最佳实践

#### 类型定义
**问题**: 使用any类型
**风险等级**: 中

**反模式**:
```typescript
// ❌ 使用any
function processData(data: any): any {
  return data.result;
}

function getUser(id: any): any {
  // ...
}
```

**最佳实践**:
```typescript
// ✅ 明确类型定义
interface User {
  id: number;
  username: string;
  email: string;
  createdAt: Date;
}

interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

function getUser(id: number): Promise<User> {
  // ...
}

function processData<T>(data: ApiResponse<T>): T {
  return data.data;
}
```

## 性能指标

| 指标 | 目标 |
|------|------|
| 响应时间(P50) | < 200ms |
| 响应时间(P99) | < 1000ms |
| 请求/秒 | > 1000 req/s |
| 内存使用 | < 512MB |
| CPU使用 | < 70% |
| 事件循环延迟 | < 100ms |

## 工具推荐

- **代码检查**: ESLint, Prettier
- **类型检查**: TypeScript tsc
- **安全审计**: npm audit, Snyk
- **性能分析**: Clinic.js, New Relic, Datadog
- **监控**: PM2, Docker健康检查
- **测试**: Jest, Mocha, Supertest

## 审查输出模板

```markdown
### [严重/高/中/低] 问题类型

**位置**: `文件路径:行号`

**问题描述**:
简明描述问题

**代码示例**:
\`\`\`javascript/typescript
// ❌ 当前代码
有问题代码
\`\`\`

**改进建议**:
\`\`\`javascript/typescript
// ✅ 建议代码
改进后代码
\`\`\`

**影响**:
- 性能: ...
- 可靠性: ...
- 可维护性: ...

**参考**: Node.js文档或最佳实践
```

## 参考资源

- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [Express Best Practices](https://expressjs.com/en/advanced/best-practice-performance.html)
- [Async/Await Best Practices](https://javascript.info/async)
- [The Art of Node](https://github.com/maxogden/art-of-node)
