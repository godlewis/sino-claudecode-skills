# Architecture Review Expert - 架构设计审查专家

## 审查范围

专注于系统架构设计、模块划分、依赖关系、设计模式应用、可扩展性、技术选型和架构原则(SOLID、DRY、KISS)。

## 核心审查维度

### 1. 分层架构

#### 关注点分离
**问题**: 业务逻辑与基础设施混杂
**风险等级**: 高

**反模式**:
```python
# ❌ 业务逻辑与数据库访问混在一起
class UserController:
    def create_user(self, username, email):
        # 业务逻辑
        if len(username) < 3:
            raise ValueError("Username too short")

        # 直接数据库访问
        conn = psycopg2.connect("...")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s)",
            (username, email)
        )
        conn.commit()

        # 发送邮件(基础设施)
        import smtplib
        server = smtplib.SMTP('smtp.example.com')
        server.sendmail(...)
```

**最佳实践**:
```python
# ✅ 分层架构
# controllers/user_controller.py
class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_user(self, username, email):
        return self.user_service.create_user(username, email)

# services/user_service.py
class UserService:
    def __init__(self,
                 user_repository: UserRepository,
                 email_service: EmailService):
        self.user_repository = user_repository
        self.email_service = email_service

    def create_user(self, username, email):
        # 业务逻辑
        if len(username) < 3:
            raise ValidationError("Username too short")

        user = User(username=username, email=email)
        user = self.user_repository.save(user)
        self.email_service.send_welcome_email(user)
        return user

# repositories/user_repository.py
class UserRepository:
    def save(self, user: User) -> User:
        # 数据库访问
        pass

# services/email_service.py
class EmailService:
    def send_welcome_email(self, user: User):
        # 邮件发送
        pass
```

**审查要点**:
- 控制器(Controller)层: 仅处理HTTP请求/响应,不包含业务逻辑
- 服务(Service)层: 核心业务逻辑
- 仓储(Repository)层: 数据访问
- 依赖方向: Controller → Service → Repository(单向依赖)

### 2. SOLID原则

#### 单一职责原则(SRP)
**问题**: 类或函数承担过多职责
**风险等级**: 高

**反模式**:
```java
// ❌ User类承担过多职责
public class User {
    public void validate() { /* 验证逻辑 */ }
    public void saveToDatabase() { /* 数据库操作 */ }
    public void sendEmail() { /* 邮件发送 */ }
    public void exportToCSV() { /* CSV导出 */ }
    public void calculateDiscount() { /* 折扣计算 */ }
}
```

**最佳实践**:
```java
// ✅ 职责分离
public class User {
    // 仅负责用户数据模型
}

public class UserValidator {
    public void validate(User user) { /* 验证逻辑 */ }
}

public class UserRepository {
    public void save(User user) { /* 数据库操作 */ }
}

public class EmailService {
    public void sendEmail(User user) { /* 邮件发送 */ }
}

public class UserExporter {
    public String exportToCSV(User user) { /* CSV导出 */ }
}

public class DiscountCalculator {
    public BigDecimal calculateDiscount(User user) { /* 折扣计算 */ }
}
```

#### 开闭原则(OCP)
**问题**: 修改现有代码添加新功能
**风险等级**: 中

**反模式**:
```typescript
// ❌ 每次添加新支付方式需修改现有代码
class PaymentProcessor {
  processPayment(type: string, amount: number) {
    if (type === 'credit_card') {
      // 信用卡逻辑
    } else if (type === 'paypal') {
      // PayPal逻辑
    } else if (type === 'wechat') {
      // 微信支付逻辑
    }
    // 每次新增支付方式都要修改这里
  }
}
```

**最佳实践**:
```typescript
// ✅ 使用接口和多态,对扩展开放
interface PaymentMethod {
  process(amount: number): Promise<boolean>;
}

class CreditCardPayment implements PaymentMethod {
  async process(amount: number): Promise<boolean> {
    // 信用卡逻辑
  }
}

class PayPalPayment implements PaymentMethod {
  async process(amount: number): Promise<boolean> {
    // PayPal逻辑
  }
}

class WeChatPayment implements PaymentMethod {
  async process(amount: number): Promise<boolean> {
    // 微信支付逻辑
  }
}

class PaymentProcessor {
  private methods: Map<string, PaymentMethod>;

  registerMethod(name: string, method: PaymentMethod) {
    this.methods.set(name, method);
  }

  async processPayment(type: string, amount: number) {
    const method = this.methods.get(type);
    if (!method) {
      throw new Error(`Unknown payment method: ${type}`);
    }
    return method.process(amount);
  }
}

// 新增支付方式无需修改现有代码
class AlipayPayment implements PaymentMethod {
  async process(amount: number): Promise<boolean> {
    // 支付宝逻辑
  }
}
```

#### 依赖倒置原则(DIP)
**问题**: 高层模块依赖低层模块
**风险等级**: 高

**反模式**:
```python
# ❌ 高层模块直接依赖低层模块实现
class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()  # 依赖具体实现
        self.cache = RedisCache()  # 依赖具体实现

    def create_order(self, order_data):
        # 业务逻辑与具体实现紧耦合
        pass
```

**最佳实践**:
```python
# ✅ 依赖抽象(接口)
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, entity):
        pass

class Cache(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

class OrderService:
    def __init__(self, db: Database, cache: Cache):
        self.db = db  # 依赖抽象
        self.cache = cache  # 依赖抽象

    def create_order(self, order_data):
        # 业务逻辑与具体实现解耦
        pass

# 具体实现
class MySQLDatabase(Database):
    def save(self, entity):
        # MySQL实现
        pass

class RedisCache(Cache):
    def get(self, key):
        # Redis实现
        pass

    def set(self, key, value):
        # Redis实现
        pass
```

### 3. 设计模式应用

#### 工厂模式
**问题**: 使用条件语句创建对象
**风险等级**: 中

**反模式**:
```javascript
// ❌ 使用条件语句创建对象
class NotificationFactory {
  createNotification(type) {
    if (type === 'email') {
      return new EmailNotification();
    } else if (type === 'sms') {
      return new SmsNotification();
    } else if (type === 'push') {
      return new PushNotification();
    }
  }
}
```

**最佳实践**:
```javascript
// ✅ 使用工厂模式
class EmailNotification {
  send(message) { /* ... */ }
}

class SmsNotification {
  send(message) { /* ... */ }
}

class PushNotification {
  send(message) { /* ... */ }
}

class NotificationFactory {
  constructor() {
    this.types = new Map();
    this.register('email', EmailNotification);
    this.register('sms', SmsNotification);
    this.register('push', PushNotification);
  }

  register(type, Class) {
    this.types.set(type, Class);
  }

  create(type) {
    const NotificationClass = this.types.get(type);
    if (!NotificationClass) {
      throw new Error(`Unknown notification type: ${type}`);
    }
    return new NotificationClass();
  }
}
```

#### 策略模式
**问题**: 使用复杂条件语句实现算法
**风险等级**: 中

**反模式**:
```java
// ❌ 复杂条件语句
public class OrderService {
    public BigDecimal calculateDiscount(Order order) {
        BigDecimal discount = BigDecimal.ZERO;

        if (order.getType() == OrderType.NEW_CUSTOMER) {
            discount = order.getTotal().multiply(new BigDecimal("0.1"));
        } else if (order.getType() == OrderType.VIP_CUSTOMER) {
            discount = order.getTotal().multiply(new BigDecimal("0.2"));
            if (order.getTotal().compareTo(new BigDecimal("1000")) > 0) {
                discount = discount.multiply(new BigDecimal("1.5"));
            }
        } else if (order.getType() == OrderType.WHOLESALE) {
            discount = order.getTotal().multiply(new BigDecimal("0.3"));
        }

        return discount;
    }
}
```

**最佳实践**:
```java
// ✅ 策略模式
public interface DiscountStrategy {
    BigDecimal calculateDiscount(Order order);
}

public class NewCustomerDiscountStrategy implements DiscountStrategy {
    public BigDecimal calculateDiscount(Order order) {
        return order.getTotal().multiply(new BigDecimal("0.1"));
    }
}

public class VipCustomerDiscountStrategy implements DiscountStrategy {
    public BigDecimal calculateDiscount(Order order) {
        BigDecimal discount = order.getTotal().multiply(new BigDecimal("0.2"));
        if (order.getTotal().compareTo(new BigDecimal("1000")) > 0) {
            discount = discount.multiply(new BigDecimal("1.5"));
        }
        return discount;
    }
}

public class WholesaleDiscountStrategy implements DiscountStrategy {
    public BigDecimal calculateDiscount(Order order) {
        return order.getTotal().multiply(new BigDecimal("0.3"));
    }
}

public class OrderService {
    private Map<OrderType, DiscountStrategy> strategies;

    public OrderService() {
        strategies = new HashMap<>();
        strategies.put(OrderType.NEW_CUSTOMER, new NewCustomerDiscountStrategy());
        strategies.put(OrderType.VIP_CUSTOMER, new VipCustomerDiscountStrategy());
        strategies.put(OrderType.WHOLESALE, new WholesaleDiscountStrategy());
    }

    public BigDecimal calculateDiscount(Order order) {
        DiscountStrategy strategy = strategies.get(order.getType());
        return strategy.calculateDiscount(order);
    }
}
```

#### 观察者模式
**问题**: 紧耦合的事件处理
**风险等级**: 中

**反模式**:
```python
# ❌ 紧耦合的事件处理
class OrderService:
    def create_order(self, order_data):
        order = Order(**order_data)
        order.save()

        # 紧耦合的事件处理
        EmailService().send_confirmation(order)
        InventoryService().update_stock(order)
        AnalyticsService().track_event('order_created', order)
        # 每次新增事件处理都要修改这里
```

**最佳实践**:
```python
# ✅ 观察者模式/事件总线
from typing import Callable, Dict, List

class EventBus:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, listener: Callable):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def publish(self, event_type: str, event_data):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(event_data)

# 事件监听器
class EmailConfirmationListener:
    def __call__(self, event):
        EmailService().send_confirmation(event.order)

class InventoryUpdateListener:
    def __call__(self, event):
        InventoryService().update_stock(event.order)

class AnalyticsListener:
    def __call__(self, event):
        AnalyticsService().track_event('order_created', event.order)

# 配置
event_bus = EventBus()
event_bus.subscribe('order.created', EmailConfirmationListener())
event_bus.subscribe('order.created', InventoryUpdateListener())
event_bus.subscribe('order.created', AnalyticsListener())

# 使用
class OrderService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def create_order(self, order_data):
        order = Order(**order_data)
        order.save()
        self.event_bus.publish('order.created', OrderCreatedEvent(order))
```

### 4. 可扩展性

#### 配置化
**问题**: 硬编码配置
**风险等级**: 中

**反模式**:
```javascript
// ❌ 硬编码配置
class PaymentService {
  constructor() {
    this.maxRetries = 3;
    this.timeout = 5000;
    this.endpoints = {
      production: 'https://api.payment.com/v1',
      sandbox: 'https://sandbox.payment.com/v1'
    };
  }
}
```

**最佳实践**:
```javascript
// ✅ 配置化
class PaymentService {
  constructor(config) {
    this.maxRetries = config.maxRetries || 3;
    this.timeout = config.timeout || 5000;
    this.endpoints = config.endpoints;
  }
}

// config/payment.js
module.exports = {
  payment: {
    maxRetries: process.env.PAYMENT_MAX_RETRIES || 3,
    timeout: process.env.PAYMENT_TIMEOUT || 5000,
    endpoints: {
      production: process.env.PAYMENT_PROD_URL,
      sandbox: process.env.PAYMENT_SANDBOX_URL
    }
  }
};
```

#### 插件化架构
**问题**: 无法在不修改核心代码的情况下扩展功能
**风险等级**: 中

**最佳实践**:
```python
# ✅ 插件化架构
from abc import ABC, abstractmethod

class Plugin(ABC):
    @abstractmethod
    def initialize(self, app):
        pass

    @abstractmethod
    def execute(self, context):
        pass

class PluginManager:
    def __init__(self):
        self.plugins = []

    def register(self, plugin: Plugin):
        self.plugins.append(plugin)

    def initialize_all(self, app):
        for plugin in self.plugins:
            plugin.initialize(app)

    def execute_all(self, context):
        for plugin in self.plugins:
            plugin.execute(context)

# 插件示例
class LoggingPlugin(Plugin):
    def initialize(self, app):
        print("Initializing Logging Plugin")

    def execute(self, context):
        print(f"Logging: {context}")

class CachePlugin(Plugin):
    def initialize(self, app):
        print("Initializing Cache Plugin")

    def execute(self, context):
        print(f"Caching: {context}")

# 使用
plugin_manager = PluginManager()
plugin_manager.register(LoggingPlugin())
plugin_manager.register(CachePlugin())
plugin_manager.initialize_all(app)
```

### 5. 数据流设计

#### CQRS(Command Query Responsibility Segregation)
**问题**: 读写操作使用相同模型
**风险等级**: 中

**反模式**:
```csharp
// ❌ 读写共用模型
public class User {
    public int Id { get; set; }
    public string Username { get; set; }
    public string Email { get; set; }
    public string PasswordHash { get; set; }  // 查询时不应暴露
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}

// 查询用户时返回了密码哈希
public User GetUser(int id) {
    return dbContext.Users.Find(id);
}
```

**最佳实践**:
```csharp
// ✅ CQRS分离读写模型
// 写模型(Command)
public class User {
    public int Id { get; set; }
    public string Username { get; set; }
    public string Email { get; set; }
    public string PasswordHash { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}

// 读模型(Query)
public class UserDto {
    public int Id { get; set; }
    public string Username { get; set; }
    public string Email { get; set; }
    public DateTime CreatedAt { get; set; }
}

// Command服务
public class UserCommandService {
    public void CreateUser(CreateUserCommand command) {
        var user = new User {
            Username = command.Username,
            Email = command.Email,
            PasswordHash = HashPassword(command.Password)
        };
        dbContext.Users.Add(user);
        dbContext.SaveChanges();
    }
}

// Query服务
public class UserQueryService {
    public UserDto GetUser(int id) {
        return dbContext.Users
            .Where(u => u.Id == id)
            .Select(u => new UserDto {
                Id = u.Id,
                Username = u.Username,
                Email = u.Email,
                CreatedAt = u.CreatedAt
            })
            .FirstOrDefault();
    }
}
```

### 6. 微服务边界

#### 服务拆分
**问题**: 服务边界不清晰,导致分布式单体
**风险等级**: 高

**审查要点**:
- **业务域驱动**: 按业务能力而非技术层次拆分
- **数据独占**: 每个服务拥有自己的数据存储
- **API网关**: 通过网关统一外部访问
- **服务通信**: 避免同步依赖,使用事件驱动

**反模式**:
```yaml
# ❌ 按技术层拆分(错误)
services:
  - user-frontend-service
  - user-backend-service
  - user-database-service
```

**最佳实践**:
```yaml
# ✅ 按业务域拆分(正确)
services:
  - user-service        # 用户管理
  - order-service       # 订单管理
  - payment-service     # 支付管理
  - notification-service # 通知服务
```

### 7. 架构反模式识别

#### 循环依赖
**问题**: 模块间循环依赖
**风险等级**: 严重

**检测方法**:
```bash
# 使用工具检测
# Python: pydeps
pydeps myproject --max-bacon=3 --cluster

# Node.js: madge
madge --circular --extensions ts,tsx src/
```

**解决方案**:
- 提取共享依赖到独立模块
- 使用依赖注入反转依赖方向
- 引入事件驱动架构解耦

#### 上帝类(God Class)
**问题**: 单个类/模块过于庞大,控制过多
**风险等级**: 高

**识别标准**:
- 类代码超过1000行
- 包含过多字段和方法
- 承担过多职责

**解决方案**:
- 按职责拆分成多个类
- 提取接口和抽象
- 应用设计模式

## 架构审查清单

### 模块化
- [ ] 代码是否按功能或层次清晰组织?
- [ ] 模块间依赖是否清晰且单向?
- [ ] 是否存在循环依赖?
- [ ] 模块边界是否稳定,不易频繁变化?

### 可扩展性
- [ ] 新增功能是否无需修改现有代码?
- [ ] 是否支持配置化?
- [ ] 是否支持插件化扩展?
- [ ] 数据库schema是否易于迁移?

### 可维护性
- [ ] 架构是否易于理解?
- [ ] 代码组织是否一致?
- [ ] 是否有清晰的分层?
- [ ] 接口是否稳定?

### 性能
- [ ] 是否考虑缓存策略?
- [ ] 是否支持水平扩展?
- [ ] 是否避免N+1查询?
- [ ] 是否使用异步处理?

### 安全性
- [ ] 层间访问是否受控?
- [ ] 敏感数据是否加密?
- [ ] 是否有审计日志?
- [ ] 访问控制是否到位?

## 审查输出模板

```markdown
### [严重/高/中/低] 架构问题

**问题描述**:
简明描述架构问题

**当前架构**:
\`\`\`
架构图或伪代码
\`\`\`

**建议架构**:
\`\`\`
改进后的架构
\`\`\`

**影响**:
- 可维护性: ...
- 可扩展性: ...
- 性能: ...

**重构建议**:
1. 步骤一
2. 步骤二
3. ...

**参考**: 相关架构模式或最佳实践
```

## 参考资源

- [Clean Architecture by Robert C. Martin](https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/)
- [Domain-Driven Design by Eric Evans](https://www.oreilly.com/library/view/domain-driven-design/0321125215/)
- [Patterns of Enterprise Application Architecture](https://www.oreilly.com/library/view/patterns-of-enterprise/0321207420/)
- [Microsoft Architecture Guide](https://docs.microsoft.com/en-us/azure/architecture/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
