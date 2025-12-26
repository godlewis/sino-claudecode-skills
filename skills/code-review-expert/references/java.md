# Java Review Expert - Java代码审查专家

## 审查范围

专注于Java代码的Clean Code原则、设计模式应用、JVM性能优化、并发编程、Spring框架最佳实践和Java 8+特性。

## 核心审查维度

### 1. 代码风格和Clean Code

#### 命名规范
**问题**: 命名不清晰或不符合Java规范
**风险等级**: 中

**反模式**:
```java
// ❌ 不清晰的命名
public class Data {
    public int d;
    public boolean flag;

    public void proc() {
        // ...
    }
}

// ❌ 违反命名规范
public class myClass {
    public static final int value = 1;  // 应该大写
}
```

**最佳实践**:
```java
// ✅ 清晰的命名
public class UserProfile {
    private int userId;
    private boolean isActive;

    public void processUserProfile() {
        // ...
    }
}

// ✅ 符合命名规范
public class MyClass {
    public static final int MAX_VALUE = 100;  // 常量大写+下划线
    private String userName;  // 驼峰命名
}
```

#### 方法长度和复杂度
**问题**: 方法过长或圈复杂度过高
**风险等级**: 高

**反模式**:
```java
// ❌ 方法过长,职责过多
public void processOrder(Order order) {
    // 200+行代码
    // 验证订单
    // 检查库存
    // 计算价格
    // 保存到数据库
    // 发送邮件
    // 更新缓存
    // 记录日志
    // ...更多逻辑
}
```

**最佳实践**:
```java
// ✅ 拆分成小方法,每个方法职责单一
public void processOrder(Order order) {
    validateOrder(order);
    checkInventory(order);
    PriceCalculation calculation = calculatePrice(order);
    saveOrder(order);
    sendConfirmationEmail(order);
    updateCache(order);
    logOrderProcessing(order);
}

private void validateOrder(Order order) {
    // 验证逻辑
}

private void checkInventory(Order order) {
    // 库存检查
}
// ...其他小方法
```

### 2. 异常处理

#### 异常捕获和处理
**问题**: 捕获过于宽泛或吞掉异常
**风险等级**: 高

**反模式**:
```java
// ❌ 捕获Exception
try {
    processOrder();
} catch (Exception e) {
    // 吞掉异常
}

// ❌ 捕获Throwable
try {
    processOrder();
} catch (Throwable t) {
    // 极其危险,包括Error
}
```

**最佳实践**:
```java
// ✅ 捕获具体异常
try {
    processOrder();
} catch (ValidationException e) {
    logger.error("Validation failed: {}", e.getMessage());
    throw new OrderProcessingException("Invalid order", e);
} catch (InventoryException e) {
    logger.error("Inventory check failed: {}", e.getMessage());
    throw new OrderProcessingException("Inventory issue", e);
}

// ✅ 使用try-with-resources
try (Connection conn = dataSource.getConnection();
     PreparedStatement stmt = conn.prepareStatement(sql)) {
    // 自动关闭资源
}
```

#### 自定义异常
**问题**: 使用通用异常而非自定义异常
**风险等级**: 中

**最佳实践**:
```java
// ✅ 定义业务异常层次
public class OrderProcessingException extends RuntimeException {
    public OrderProcessingException(String message) {
        super(message);
    }

    public OrderProcessingException(String message, Throwable cause) {
        super(message, cause);
    }
}

public class InsufficientInventoryException extends OrderProcessingException {
    private final String productId;
    private final int requestedQuantity;
    private final int availableQuantity;

    public InsufficientInventoryException(String productId,
                                         int requestedQuantity,
                                         int availableQuantity) {
        super(String.format("Insufficient inventory for product %s: requested=%d, available=%d",
                           productId, requestedQuantity, availableQuantity));
        this.productId = productId;
        this.requestedQuantity = requestedQuantity;
        this.availableQuantity = availableQuantity;
    }

    // getters...
}
```

### 3. 并发编程

#### 线程安全
**问题**: 共享可变状态未正确同步
**风险等级**: 严重

**反模式**:
```java
// ❌ 非线程安全的共享状态
public class Counter {
    private int count = 0;

    public void increment() {
        count++;  // 竞态条件
    }

    public int getCount() {
        return count;
    }
}
```

**最佳实践**:
```java
// ✅ 使用Atomic类
public class Counter {
    private final AtomicInteger count = new AtomicInteger(0);

    public void increment() {
        count.incrementAndGet();
    }

    public int getCount() {
        return count.get();
    }
}

// ✅ 使用锁
public class Counter {
    private int count = 0;
    private final Object lock = new Object();

    public void increment() {
        synchronized (lock) {
            count++;
        }
    }

    public int getCount() {
        synchronized (lock) {
            return count;
        }
    }
}
```

#### 并发集合使用
**问题**: 在多线程环境使用非线程安全集合
**风险等级**: 高

**反模式**:
```java
// ❌ 非线程安全的集合
public class UserService {
    private List<User> users = new ArrayList<>();

    public void addUser(User user) {
        users.add(user);  // 并发问题
    }
}
```

**最佳实践**:
```java
// ✅ 使用并发集合
import java.util.concurrent.*;

public class UserService {
    private final List<User> users = new CopyOnWriteArrayList<>();
    // 或
    private final Map<String, User> userMap = new ConcurrentHashMap<>();

    public void addUser(User user) {
        users.add(user);  // 线程安全
    }
}
```

#### 线程池使用
**问题**: 直接创建线程或不当使用线程池
**风险等级**: 高

**反模式**:
```java
// ❌ 直接创建线程
for (int i = 0; i < 1000; i++) {
    new Thread(() -> processTask()).start();  // 创建过多线程
}
```

**最佳实践**:
```java
// ✅ 使用线程池
import java.util.concurrent.*;

public class TaskProcessor {
    private final ExecutorService executorService;

    public TaskProcessor() {
        // 根据业务类型选择合适的线程池
        this.executorService = new ThreadPoolExecutor(
            10,  // 核心线程数
            50,  // 最大线程数
            60L, TimeUnit.SECONDS,  // 空闲线程存活时间
            new LinkedBlockingQueue<>(1000),  // 任务队列
            new ThreadPoolExecutor.CallerRunsPolicy()  // 拒绝策略
        );
    }

    public void submitTask(Runnable task) {
        executorService.submit(task);
    }

    public void shutdown() {
        executorService.shutdown();
        try {
            if (!executorService.awaitTermination(60, TimeUnit.SECONDS)) {
                executorService.shutdownNow();
            }
        } catch (InterruptedException e) {
            executorService.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
```

### 4. JVM性能优化

#### 字符串拼接
**问题**: 在循环中使用+拼接字符串
**风险等级**: 中

**反模式**:
```java
// ❌ 在循环中拼接字符串
String result = "";
for (Item item : items) {
    result += item.toString();  // 每次创建新String对象
}
```

**最佳实践**:
```java
// ✅ 使用StringBuilder
StringBuilder sb = new StringBuilder();
for (Item item : items) {
    sb.append(item);
}
String result = sb.toString();
```

#### 集合初始化
**问题**: 集合未指定初始容量
**风险等级**: 中

**反模式**:
```java
// ❌ 未指定初始容量,可能多次扩容
List<String> list = new ArrayList<>();
for (int i = 0; i < 10000; i++) {
    list.add("item" + i);  // 多次扩容和数组拷贝
}
```

**最佳实践**:
```java
// ✅ 指定初始容量
List<String> list = new ArrayList<>(10000);
for (int i = 0; i < 10000; i++) {
    list.add("item" + i);
}

// ✅ HashMap也类似
Map<String, User> userMap = new HashMap<>(expectedSize);
```

#### 流(Stream)使用
**问题**: 不恰当使用Stream API
**风险等级**: 中

**反模式**:
```java
// ❌ 简单操作使用Stream(性能差)
List<String> names = new ArrayList<>();
for (User user : users) {
    names.add(user.getName());
}
```

**最佳实践**:
```java
// ✅ 简单操作使用传统循环
List<String> names = new ArrayList<>(users.size());
for (User user : users) {
    names.add(user.getName());
}

// ✅ 复杂操作使用Stream
Map<String, List<User>> usersByCity = users.stream()
    .filter(User::isActive)
    .collect(Collectors.groupingBy(User::getCity));
```

### 5. Spring框架最佳实践

#### 依赖注入
**问题**: 使用字段注入
**风险等级**: 中

**反模式**:
```java
// ❌ 字段注入
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EmailService emailService;
}
```

**最佳实践**:
```java
// ✅ 构造器注入(推荐)
@Service
@RequiredArgsConstructor  // Lombok
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
}

// 或显式构造器
@Service
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;

    public UserService(UserRepository userRepository,
                      EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
}
```

#### Transaction使用
**问题**: 缺少@Transactional或使用不当
**风险等级**: 高

**反模式**:
```java
// ❌ 缺少事务
@Service
public class AccountService {
    public void transfer(Long fromId, Long toId, BigDecimal amount) {
        accountDao.withdraw(fromId, amount);
        // 如果这里失败,数据不一致
        accountDao.deposit(toId, amount);
    }
}
```

**最佳实践**:
```java
// ✅ 添加事务
@Service
public class AccountService {
    @Transactional
    public void transfer(Long fromId, Long toId, BigDecimal amount) {
        accountDao.withdraw(fromId, amount);
        accountDao.deposit(toId, amount);
    }
}
```

#### 事务传播
**问题**: 不了解事务传播行为
**风险等级**: 中

**最佳实践**:
```java
// ✅ 明确指定传播行为
@Service
public class OrderService {
    // REQUIRED: 默认,加入现有事务或创建新事务
    @Transactional(propagation = Propagation.REQUIRED)
    public void placeOrder(Order order) {
        // ...
    }

    // REQUIRES_NEW: 总是创建新事务
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logAudit(String message) {
        // 独立事务,即使外部事务回滚也不影响
    }

    // NOT_SUPPORTED: 非事务执行
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public List<Order> searchOrders(String keyword) {
        // 只读操作,不需要事务
    }
}
```

### 6. 设计模式应用

#### 单例模式
**问题**: 单例实现不线程安全或过度使用
**风险等级**: 高

**反模式**:
```java
// ❌ 延迟初始化但非线程安全
public class Singleton {
    private static Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {  // 竞态条件
            instance = new Singleton();
        }
        return instance;
    }
}
```

**最佳实践**:
```java
// ✅ 使用枚举(推荐)
public enum Singleton {
    INSTANCE;

    public void doSomething() {
        // ...
    }
}

// ✅ 或使用双重检查锁定
public class Singleton {
    private static volatile Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

#### Builder模式
**问题**: 构造器参数过多
**风险等级**: 中

**反模式**:
```java
// ❌ 构造器参数过多
public class User {
    public User(String firstName, String lastName, String email,
                String phone, String address, Integer age, ...) {
        // 参数过多,难以使用
    }
}
```

**最佳实践**:
```java
// ✅ 使用Builder模式
@Builder
public class User {
    private String firstName;
    private String lastName;
    private String email;
    private String phone;
    private String address;
    private Integer age;
}

// 使用
User user = User.builder()
    .firstName("John")
    .lastName("Doe")
    .email("john@example.com")
    .age(30)
    .build();
```

### 7. 资源管理

#### IO资源关闭
**问题**: 未正确关闭IO资源
**风险等级**: 高

**反模式**:
```java
// ❌ 可能资源泄露
FileInputStream fis = new FileInputStream("file.txt");
// 如果异常,文件未关闭
```

**最佳实践**:
```java
// ✅ 使用try-with-resources
try (FileInputStream fis = new FileInputStream("file.txt");
     BufferedInputStream bis = new BufferedInputStream(fis)) {
    // 自动关闭资源
}
```

### 8. Java 8+特性使用

#### Optional使用
**问题**: Optional使用不当
**风险等级**: 中

**反模式**:
```java
// ❌ 永远不要返回null的Optional
public Optional<User> findUser(Long id) {
    User user = userRepository.findById(id);
    if (user == null) {
        return null;  // ❌ 返回null
    }
    return Optional.of(user);

    // ❌ 直接调用get()
    Optional<User> userOpt = findUser(1L);
    User user = userOpt.get();  // 可能抛出NoSuchElementException
}

// ❌ Optional作为字段
public class User {
    private Optional<String> email;  // ❌ 不要这样做
}
```

**最佳实践**:
```java
// ✅ 正确使用Optional
public Optional<User> findUser(Long id) {
    return Optional.ofNullable(userRepository.findById(id));
}

// ✅ 链式调用
Optional<String> email = findUser(userId)
    .map(User::getEmail)
    .filter(StringUtils::isNotBlank)
    .orElse("default@example.com");

// ✅ orElseGet延迟求值
User user = userOpt.orElseGet(() -> createDefaultUser());
```

#### Stream API
**最佳实践**:
```java
// ✅ 使用Stream处理集合
List<String> activeUsernames = users.stream()
    .filter(User::isActive)
    .map(User::getUsername)
    .distinct()
    .sorted()
    .collect(Collectors.toList());

// ✅ 使用原始类型Stream避免装箱
LongSummaryStatistics stats = users.stream()
    .mapToLong(User::getId)
    .summaryStatistics();
```

### 9. 代码质量工具

#### 使用Lombok
**最佳实践**:
```java
// ✅ 减少样板代码
@Data  // getter/setter/equals/hashCode/toString
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
@AllArgsConstructor
@RequiredArgsConstructor
public class User {
    @EqualsAndHashCode.Include
    private Long id;

    @NonNull
    private String username;

    private String email;
}
```

## 审查输出模板

```markdown
### [严重/高/中/低] 问题类型

**位置**: `文件路径:行号`

**问题描述**:
简明描述问题

**代码示例**:
\`\`\`java
// ❌ 当前代码
有问题代码
\`\`\`

**改进建议**:
\`\`\`java
// ✅ 建议代码
改进后代码
\`\`\`

**影响**:
- 代码质量: ...
- 性能: ...
- 可维护性: ...

**参考**: Effective Java章节或相关文档
```

## 工具推荐

- **代码检查**: SonarQube, Checkstyle, PMD, SpotBugs
- **代码格式化**: Google Java Format, Eclipse JDT
- **静态分析**: Error Prone, NullAway
- **性能分析**: JProfiler, VisualVM, Java Mission Planner
- **测试**: JUnit 5, Mockito, TestContainers

## 参考资源

- [Effective Java by Joshua Bloch](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/)
- [Clean Code by Robert C. Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [Java Code Conventions](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html)
- [Spring Framework Best Practices](https://spring.io/guides)
