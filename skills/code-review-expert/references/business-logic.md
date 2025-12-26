# Business Logic Review Expert - 业务逻辑审查专家

## 审查范围

专注于业务逻辑正确性、业务规则实现、边界条件处理、业务流程合理性、数据一致性和业务需求符合度。

## 核心审查维度

### 1. 业务规则验证

#### 数据验证
**问题**: 业务规则验证不完整或缺失
**风险等级**: 高

**反模式**:
```javascript
// ❌ 缺少业务规则验证
function createOrder(orderData) {
  const order = new Order(orderData);
  order.save();
  return order;
}
```

**最佳实践**:
```javascript
// ✅ 完整的业务规则验证
function createOrder(orderData) {
  // 验证商品存在
  const products = validateProducts(orderData.items);

  // 验证库存
  validateInventory(products);

  // 验证最小订单金额
  if (orderData.total < MIN_ORDER_AMOUNT) {
    throw new BusinessRuleError(
      `Order total must be at least ${MIN_ORDER_AMOUNT}`
    );
  }

  // 验证配送地址
  if (!isValidDeliveryAddress(orderData.address)) {
    throw new BusinessRuleError('Invalid delivery address');
  }

  // VIP客户特殊验证
  if (orderData.customer.isVip) {
    validateVipOrder(orderData);
  }

  const order = new Order(orderData);
  order.save();
  return order;
}

function validateInventory(items) {
  for (const item of items) {
    if (item.quantity > item.product.maxOrderQuantity) {
      throw new BusinessRuleError(
        `Maximum order quantity for ${item.product.name} is ${item.product.maxOrderQuantity}`
      );
    }
    if (item.quantity > item.product.stock) {
      throw new InsufficientStockError(
        `Insufficient stock for ${item.product.name}. Available: ${item.product.stock}`
      );
    }
  }
}
```

**审查要点**:
- 所有输入参数是否验证?
- 业务约束是否 enforced?
- 边界值是否处理(min, max)?
- 特殊情况是否考虑?

### 2. 业务流程完整性

#### 状态机
**问题**: 状态转换逻辑不清晰或允许非法转换
**风险等级**: 高

**反模式**:
```python
# ❌ 任意状态转换
class Order:
    def cancel(self):
        self.status = 'cancelled'

    def ship(self):
        self.status = 'shipped'

    def complete(self):
        self.status = 'completed'

# 可以直接从pending跳到completed,跳过shipped
```

**最佳实践**:
```python
# ✅ 使用状态机模式
from enum import Enum

class OrderStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'

# 定义合法的状态转换
VALID_TRANSITIONS = {
    OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
    OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
    OrderStatus.SHIPPED: [OrderStatus.DELIVERED, OrderStatus.REFUNDED],
    OrderStatus.DELIVERED: [OrderStatus.REFUNDED],
    OrderStatus.CANCELLED: [],  # 终态
    OrderStatus.REFUNDED: []    # 终态
}

class Order:
    def __init__(self):
        self.status = OrderStatus.PENDING
        self.status_history = [OrderStatus.PENDING]

    def transition_to(self, new_status):
        """执行状态转换"""
        if new_status not in VALID_TRANSITIONS[self.status]:
            raise InvalidStateTransitionError(
                f"Cannot transition from {self.status.value} to {new_status.value}"
            )

        # 执行状态转换前的业务逻辑
        self._before_status_transition(new_status)

        # 记录状态历史
        self.status_history.append(new_status)
        self.status = new_status

        # 执行状态转换后的业务逻辑
        self._after_status_transition(new_status)

    def _before_status_transition(self, new_status):
        """状态转换前的逻辑"""
        if new_status == OrderStatus.SHIPPED:
            self._validate_shipping_details()
        elif new_status == OrderStatus.REFUNDED:
            self._validate_refund_eligibility()

    def _after_status_transition(self, new_status):
        """状态转换后的逻辑"""
        if new_status == OrderStatus.CONFIRMED:
            self._reserve_inventory()
        elif new_status == OrderStatus.CANCELLED:
            self._release_inventory()
            self._process_refund()

    def cancel(self):
        """取消订单"""
        if not self.can_cancel():
            raise OrderCannotBeCancelledError(
                f"Order in {self.status.value} cannot be cancelled"
            )
        self.transition_to(OrderStatus.CANCELLED)

    def can_cancel(self):
        """检查是否可以取消"""
        return self.status in [
            OrderStatus.PENDING,
            OrderStatus.CONFIRMED
        ]
```

### 3. 业务计算正确性

#### 价格计算
**问题**: 价格计算逻辑错误或精度问题
**风险等级**: 严重

**反模式**:
```javascript
// ❌ 浮点数精度问题
function calculateTotalPrice(items) {
  let total = 0;
  for (const item of items) {
    total += item.price * item.quantity;  // 浮点数累加可能产生精度问题
  }
  return total;
}

// ❌ 折扣计算顺序错误
function applyDiscounts(price, user) {
  if (user.isVip) {
    price = price * 0.9;  // VIP 10% off
  }
  if (hasCoupon) {
    price = price - 10;   // 减10元
  }
  return price;
  // 问题:先减固定金额再打折更优惠
}
```

**最佳实践**:
```javascript
// ✅ 使用整数或decimal处理金额
function calculateTotalPrice(items) {
  let totalCents = 0;
  for (const item of items) {
    totalCents += item.priceCents * item.quantity;
  }
  return {
    totalCents,
    totalDollars: totalCents / 100
  };
}

// ✅ 正确的折扣计算顺序
function calculateDiscountedPrice(basePriceCents, user, coupon) {
  // 1. 应用百分比折扣(VIP折扣等)
  let price = basePriceCents;

  if (user.isVip) {
    price = applyPercentageDiscount(price, 10);  // 10% off
  }

  // 2. 应用固定金额折扣(优惠券等)
  if (coupon) {
    price = applyFixedDiscount(price, coupon.amountCents);
  }

  // 3. 确保价格不为负
  price = Math.max(0, price);

  return {
    priceCents: price,
    priceDollars: price / 100,
    discounts: {
      vipDiscount: basePriceCents - applyPercentageDiscount(basePriceCents, 10),
      couponDiscount: coupon ? coupon.amountCents : 0
    }
  };
}

function applyPercentageDiscount(priceCents, percentage) {
  return Math.round(priceCents * (100 - percentage) / 100);
}

function applyFixedDiscount(priceCents, discountCents) {
  return Math.max(0, priceCents - discountCents);
}
```

#### 税费计算
**问题**: 税费计算不符合业务规则
**风险等级**: 高

**最佳实践**:
```python
# ✅ 正确的税费计算
from decimal import Decimal
from typing import List
from dataclasses import dataclass

@dataclass
class TaxRate:
    region: str
    rate: Decimal  # 税率,如0.13表示13%
    applicable_categories: List[str]  # 适用商品类别

@dataclass
class LineItem:
    product_id: str
    category: str
    quantity: int
    unit_price: Decimal  # 单价(不含税)

class TaxCalculator:
    def __init__(self, tax_rates: List[TaxRate]):
        self.tax_rates = tax_rates

    def calculate_tax(self,
                     items: List[LineItem],
                     region: str) -> Dict[str, Dict]:
        """计算税费"""
        applicable_rate = self._get_tax_rate(region)

        tax_details = {}
        total_tax = Decimal('0')
        total_subtotal = Decimal('0')

        for item in items:
            if item.category not in applicable_rate.applicable_categories:
                # 该商品类别不征税
                continue

            subtotal = item.unit_price * item.quantity
            tax = subtotal * applicable_rate.rate

            # 四舍五入到分
            tax = tax.quantize(Decimal('0.01'))

            tax_details[item.product_id] = {
                'subtotal': subtotal,
                'tax_rate': applicable_rate.rate,
                'tax': tax,
                'total': subtotal + tax
            }

            total_tax += tax
            total_subtotal += subtotal

        return {
            'items': tax_details,
            'summary': {
                'subtotal': total_subtotal,
                'total_tax': total_tax,
                'total': total_subtotal + total_tax,
                'tax_rate': applicable_rate.rate
            }
        }

    def _get_tax_rate(self, region: str) -> TaxRate:
        """获取指定地区的税率"""
        for rate in self.tax_rates:
            if rate.region == region:
                return rate
        raise ValueError(f"No tax rate found for region: {region}")
```

### 4. 边界条件和异常情况

#### 空值处理
**问题**: 未正确处理null/undefined/空集合
**风险等级**: 高

**反模式**:
```javascript
// ❌ 未处理空值
function getFullName(user) {
  return user.firstName + ' ' + user.lastName;  // user可能为null
}

// ❌ 空字符串检查不完整
function isValidEmail(email) {
  return email && email.length > 0;  // ''为false但' '为true
}
```

**最佳实践**:
```javascript
// ✅ 正确处理空值
function getFullName(user) {
  if (!user) {
    return 'Guest';
  }

  const firstName = user.firstName || '';
  const lastName = user.lastName || '';
  const fullName = `${firstName} ${lastName}`.trim();

  return fullName || 'Unknown User';
}

// ✅ 完整的空值检查
function isValidEmail(email) {
  if (!email || typeof email !== 'string') {
    return false;
  }

  const trimmed = email.trim();
  if (trimmed.length === 0) {
    return false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(trimmed);
}

// ✅ 使用Optional模式
class Optional {
  constructor(value) {
    this.value = value;
  }

  static of(value) {
    return new Optional(value);
  }

  static empty() {
    return new Optional(null);
  }

  isPresent() {
    return this.value !== null && this.value !== undefined;
  }

  orElse(defaultValue) {
    return this.isPresent() ? this.value : defaultValue;
  }

  map(fn) {
    return this.isPresent()
      ? Optional.of(fn(this.value))
      : Optional.empty();
  }

  filter(predicate) {
    return this.isPresent() && predicate(this.value)
      ? this
      : Optional.empty();
  }
}

// 使用
const userName = Optional.of(user)
  .map(u => u.name)
  .filter(name => name.length > 0)
  .orElse('Guest');
```

#### 极端值处理
**问题**: 未处理极大/极小值
**风险等级**: 中

**最佳实践**:
```python
# ✅ 处理极端值
from datetime import datetime, timedelta
from decimal import Decimal

def calculate_discounted_price(
    original_price: Decimal,
    discount_percentage: Decimal
) -> Decimal:
    """计算折扣后价格"""

    # 验证价格范围
    if original_price < 0:
        raise ValueError("Price cannot be negative")

    if original_price > 1000000:  # 100万元
        raise ValueError("Price exceeds maximum allowed")

    # 验证折扣百分比
    if discount_percentage < 0:
        raise ValueError("Discount percentage cannot be negative")

    if discount_percentage > 100:
        raise ValueError("Discount percentage cannot exceed 100")

    # 计算折扣
    discount_amount = original_price * discount_percentage / 100
    discounted_price = original_price - discount_amount

    # 确保不为负
    return max(discounted_price, Decimal('0'))

def calculate_delivery_date(
    order_date: datetime,
    delivery_days: int
) -> datetime:
    """计算配送日期"""

    if delivery_days < 0:
        raise ValueError("Delivery days cannot be negative")

    if delivery_days > 365:
        raise ValueError("Delivery days cannot exceed 365")

    delivery_date = order_date + timedelta(days=delivery_days)

    # 不允许周末配送
    while delivery_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
        delivery_date += timedelta(days=1)

    return delivery_date
```

### 5. 数据一致性

#### 事务边界
**问题**: 缺少事务导致数据不一致
**风险等级**: 严重

**反模式**:
```python
# ❌ 缺少事务
def transfer_money(from_account_id, to_account_id, amount):
    from_account = Account.objects.get(id=from_account_id)
    to_account = Account.objects.get(id=to_account_id)

    from_account.balance -= amount
    from_account.save()  # 如果这里成功,下面失败怎么办?

    to_account.balance += amount
    to_account.save()

    # 数据不一致!
```

**最佳实践**:
```python
# ✅ 使用事务
from django.db import transaction

@transaction.atomic
def transfer_money(from_account_id, to_account_id, amount):
    """转账操作(原子性)"""

    # 使用select_for_update锁定记录
    from_account = Account.objects.select_for_update().get(id=from_account_id)
    to_account = Account.objects.select_for_update().get(id=to_account_id)

    # 业务规则验证
    if from_account.balance < amount:
        raise InsufficientFundsError(
            f"Account {from_account_id} has insufficient balance"
        )

    if amount <= 0:
        raise InvalidAmountError("Transfer amount must be positive")

    if from_account_id == to_account_id:
        raise InvalidTransferError("Cannot transfer to same account")

    # 执行转账
    from_account.balance -= amount
    to_account.balance += amount

    from_account.save()
    to_account.save()

    # 记录交易日志
    TransactionLog.objects.create(
        from_account=from_account,
        to_account=to_account,
        amount=amount,
        type='TRANSFER'
    )

    return {
        'from_balance': from_account.balance,
        'to_balance': to_account.balance
    }
```

### 6. 业务规则配置化

#### 规则硬编码
**问题**: 业务规则硬编码,难以维护
**风险等级**: 中

**反模式**:
```java
// ❌ 硬编码业务规则
public class OrderService {
    public void validateOrder(Order order) {
        if (order.getTotalAmount().compareTo(new BigDecimal("100")) < 0) {
            throw new ValidationException("Minimum order amount is 100");
        }

        if (order.getItems().size() > 50) {
            throw new ValidationException("Maximum 50 items per order");
        }

        if (order.getDeliveryAddress().getPostalCode().startsWith("100")) {
            order.setShippingFee(new BigDecimal("10"));
        } else {
            order.setShippingFee(new BigDecimal("20"));
        }
    }
}
```

**最佳实践**:
```java
// ✅ 配置化业务规则
@Configuration
@ConfigurationProperties(prefix = "business.rules")
public class BusinessRules {
    private BigDecimal minOrderAmount = new BigDecimal("100");
    private int maxItemsPerOrder = 50;
    private Map<String, ShippingRule> shippingRules = new HashMap<>();

    // getters and setters

    public static class ShippingRule {
        private String postalCodePrefix;
        private BigDecimal fee;
        // getters and setters
    }
}

@Service
public class OrderService {
    private final BusinessRules businessRules;

    public OrderService(BusinessRules businessRules) {
        this.businessRules = businessRules;
    }

    public void validateOrder(Order order) {
        if (order.getTotalAmount().compareTo(businessRules.getMinOrderAmount()) < 0) {
            throw new ValidationException(String.format(
                "Minimum order amount is %s",
                businessRules.getMinOrderAmount()
            ));
        }

        if (order.getItems().size() > businessRules.getMaxItemsPerOrder()) {
            throw new ValidationException(String.format(
                "Maximum %d items per order",
                businessRules.getMaxItemsPerOrder()
            ));
        }
    }

    public void calculateShippingFee(Order order) {
        String postalCode = order.getDeliveryAddress().getPostalCode();

        BigDecimal fee = businessRules.getShippingRules()
            .entrySet()
            .stream()
            .filter(entry -> postalCode.startsWith(entry.getKey()))
            .findFirst()
            .map(entry -> entry.getValue().getFee())
            .orElse(new BigDecimal("20"));  // 默认运费

        order.setShippingFee(fee);
    }
}

# application.yml
business:
  rules:
    min-order-amount: 100
    max-items-per-order: 50
    shipping-rules:
      "100": { postal-code-prefix: "100", fee: 10 }
      "200": { postal-code-prefix: "200", fee: 15 }
```

### 7. 业务日志和审计

#### 关键操作审计
**问题**: 缺少业务操作日志
**风险等级**: 中

**最佳实践**:
```python
# ✅ 业务操作审计
import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)

class BusinessEventLogger:
    """业务事件记录器"""

    def log_order_created(self, order, user):
        """记录订单创建事件"""
        self._log_event(
            event_type='ORDER_CREATED',
            entity_type='Order',
            entity_id=order.id,
            user_id=user.id,
            data={
                'order_total': float(order.total_amount),
                'item_count': order.items.count(),
                'customer_id': order.customer.id,
                'delivery_address': order.delivery_address.to_dict()
            }
        )

    def log_payment_processed(self, payment, user):
        """记录支付处理事件"""
        self._log_event(
            event_type='PAYMENT_PROCESSED',
            entity_type='Payment',
            entity_id=payment.id,
            user_id=user.id,
            data={
                'order_id': payment.order.id,
                'amount': float(payment.amount),
                'payment_method': payment.method,
                'status': payment.status
            }
        )

    def log_order_cancelled(self, order, user, reason):
        """记录订单取消事件"""
        self._log_event(
            event_type='ORDER_CANCELLED',
            entity_type='Order',
            entity_id=order.id,
            user_id=user.id,
            data={
                'reason': reason,
                'order_status_before': order.status,
                'refund_amount': float(order.refund_amount) if order.refund_amount else None
            }
        )

    def _log_event(self,
                   event_type: str,
                   entity_type: str,
                   entity_id: Any,
                   user_id: Any,
                   data: Dict):
        """记录业务事件"""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'entity_type': entity_type,
            'entity_id': str(entity_id),
            'user_id': str(user_id),
            'data': data,
            'ip_address': self._get_current_request_ip(),
            'user_agent': self._get_current_user_agent()
        }

        logger.info(f"Business Event: {event_type}", extra=event)

        # 保存到审计表
        BusinessAuditLog.objects.create(**event)

    def _get_current_request_ip(self):
        """获取当前请求IP"""
        # 实现获取IP的逻辑
        pass

    def _get_current_user_agent(self):
        """获取当前User-Agent"""
        # 实现获取User-Agent的逻辑
        pass
```

## 业务审查清单

### 业务规则
- [ ] 所有业务规则是否明确实现?
- [ ] 业务规则验证是否在正确的层次?
- [ ] 是否有规则引擎或配置化?
- [ ] 规则冲突如何解决?

### 数据完整性
- [ ] 事务边界是否正确?
- [ ] 是否有并发控制?
- [ ] 数据一致性如何保证?
- [ ] 是否有审计日志?

### 边界条件
- [ ] 空值是否处理?
- [ ] 极端值是否处理?
- [ ] 异常情况是否考虑?
- [ ] 是否有降级策略?

### 计算正确性
- [ ] 数值计算精度是否正确?
- [ ] 货币计算是否使用decimal?
- [ ] 日期时间是否考虑时区?
- [ ] 百分比计算是否正确?

### 业务流程
- [ ] 状态机是否清晰?
- [ ] 状态转换是否合法?
- [ ] 是否有补偿机制?
- [ ] 是否有回滚策略?

## 审查输出模板

```markdown
### [严重/高/中/低] 业务逻辑问题

**位置**: `文件路径:行号`

**业务规则**:
描述相关业务规则

**问题描述**:
简明描述业务逻辑问题

**代码示例**:
\`\`\`language
# ❌ 当前实现
有问题代码
\`\`\`

**改进建议**:
\`\`\`language
# ✅ 建议实现
正确实现
\`\`\`

**业务影响**:
- 财务损失: ...
- 客户体验: ...
- 合规风险: ...

**测试建议**:
1. 边界条件测试: ...
2. 异常情况测试: ...
3. 业务场景测试: ...
```

## 参考资源

- [Domain-Driven Design by Eric Evans](https://www.oreilly.com/library/view/domain-driven-design/0321125215/)
- [Implementing Domain-Driven Design by Vaughn Vernon](https://www.oreilly.com/library/view/implementing-domain-driven/9780133039906/)
- [Business Rule Patterns](https://www.amazon.com/Business-Rule-Patterns-Name-Technology/dp/3110165946)
