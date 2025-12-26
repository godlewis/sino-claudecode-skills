# Python Review Expert - Python代码审查专家

## 审查范围

专注于Python代码的PEP 8规范、Pythonic风格、类型注解、异步编程、包管理和Python特有的最佳实践。

## 核心审查维度

### 1. 代码风格和PEP 8

#### PEP 8合规性
**问题**: 不符合PEP 8规范
**风险等级**: 中

**反模式**:
```python
# ❌ 违反PEP 8
def CalculateData( input_data ):
    Result=[]
    for item in input_data:
        Result.append(item*2)
    return Result
```

**最佳实践**:
```python
# ✅ 遵循PEP 8
def calculate_data(input_data):
    """Calculate and double input data."""
    result = []
    for item in input_data:
        result.append(item * 2)
    return result
```

**审查要点**:
- 使用snake_case命名函数和变量
- 使用PascalCase命名类
- 每级缩进4个空格
- 一行不超过79字符(文档字符串/注释不超过72)
- 空行使用恰当(函数间2行,类内方法间1行)

#### Import顺序
**问题**: Import顺序混乱
**风险等级**: 低

**最佳实践**:
```python
# ✅ 正确的import顺序
# 1. 标准库
import os
import sys
from typing import List, Optional

# 2. 第三方库
import requests
from fastapi import FastAPI

# 3. 本地应用
from .models import User
from .utils import format_data
```

### 2. Pythonic代码

#### 列表推导式
**问题**: 不使用列表推导式或误用
**风险等级**: 中

**反模式**:
```python
# ❌ 不Pythonic
result = []
for item in items:
    if item > 0:
        result.append(item * 2)
```

**最佳实践**:
```python
# ✅ 使用列表推导式
result = [item * 2 for item in items if item > 0]

# 但注意:可读性优先,复杂逻辑用for循环
```

#### 上下文管理器
**问题**: 未使用with语句管理资源
**风险等级**: 高

**反模式**:
```python
# ❌ 可能资源泄露
f = open('file.txt')
try:
    data = f.read()
finally:
    f.close()
```

**最佳实践**:
```python
# ✅ 使用with语句
with open('file.txt') as f:
    data = f.read()
```

#### 装饰器使用
**问题**: 重复的样板代码可提取为装饰器
**风险等级**: 中

**最佳实践**:
```python
# ✅ 使用装饰器消除重复
import time
from functools import wraps

def timing_decorator(func):
    """Measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@timing_decorator
def process_data():
    # ...
```

### 3. 类型注解

#### 类型提示
**问题**: 缺少类型注解
**风险等级**: 中

**反模式**:
```python
# ❌ 缺少类型注解
def calculate(a, b):
    return a + b

def process_users(users):
    # users是什么类型?
    pass
```

**最佳实践**:
```python
# ✅ 添加类型注解
from typing import List, Dict, Optional, Union

def calculate(a: int, b: int) -> int:
    return a + b

def process_users(users: List[Dict[str, Union[str, int]]]) -> Optional[str]:
    """Process list of user dictionaries."""
    pass
```

**审查要点**:
- 所有公共函数必须有类型注解
- 使用typing模块的泛型类型(List, Dict, Optional等)
- 复杂类型使用TypeAlias定义
- Python 3.10+使用新语法(`list[int]`而非`List[int]`)

### 4. 异常处理

#### 具体异常捕获
**问题**: 捕获过于宽泛的异常
**风险等级**: 高

**反模式**:
```python
# ❌ 捕获所有异常
try:
    process_data()
except Exception:
    pass  # 静默失败,掩盖问题
```

**最佳实践**:
```python
# ✅ 捕获具体异常
try:
    process_data()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
except KeyError as e:
    logger.error(f"Missing key: {e}")
    raise
```

#### 自定义异常
**问题**: 使用通用异常而非自定义异常
**风险等级**: 中

**最佳实践**:
```python
# ✅ 定义业务异常
class UserNotFoundError(Exception):
    """Raised when user is not found."""

class InvalidPasswordError(Exception):
    """Raised when password validation fails."""

def login(username: str, password: str) -> User:
    user = db.get_user(username)
    if not user:
        raise UserNotFoundError(f"User {username} not found")
    if not user.verify_password(password):
        raise InvalidPasswordError("Invalid password")
    return user
```

### 5. 资源管理

#### 文件操作
**问题**: 大文件一次性加载到内存
**风险等级**: 高

**反模式**:
```python
# ❌ 加载大文件到内存
with open('large_file.txt') as f:
    content = f.read()  # 可能耗尽内存
```

**最佳实践**:
```python
# ✅ 逐行处理
with open('large_file.txt') as f:
    for line in f:  # 逐行读取
        process_line(line)

# ✅ 分块读取
CHUNK_SIZE = 8192
with open('large_file.txt', 'rb') as f:
    while chunk := f.read(CHUNK_SIZE):
        process_chunk(chunk)
```

#### 数据库连接池
**问题**: 未使用连接池
**风险等级**: 高

**最佳实践**:
```python
# ✅ 使用SQLAlchemy连接池
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # 检查连接有效性
    pool_recycle=3600   # 1小时后回收连接
)
```

### 6. 异步编程

#### async/await使用
**问题**: 混用同步和异步代码
**风险等级**: 高

**反模式**:
```python
# ❌ 在async函数中阻塞
async def fetch_data():
    time.sleep(2)  # 阻塞事件循环
    response = requests.get(url)  # 阻塞IO
    return response
```

**最佳实践**:
```python
# ✅ 使用异步库
import asyncio
import aiohttp

async def fetch_data():
    await asyncio.sleep(2)  # 非阻塞
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

#### 并发控制
**问题**: 无限制的并发导致资源耗尽
**风险等级**: 高

**最佳实践**:
```python
# ✅ 限制并发数
import asyncio

async def fetch_with_semaphore(urls):
    semaphore = asyncio.Semaphore(10)  # 最多10个并发

    async def fetch(url):
        async with semaphore:
            return await fetch_data(url)

    tasks = [fetch(url) for url in urls]
    return await asyncio.gather(*tasks)
```

### 7. 包管理

#### 依赖管理
**问题**: 依赖版本未锁定
**风险等级**: 高

**最佳实践**:
```bash
# ✅ 使用虚拟环境
python -m venv venv
source venv/bin/activate

# ✅ 使用pip-tools或poetry
pip install pip-tools
pip-compile requirements.in  # 生成requirements.txt
pip-sync  # 同步依赖

# 或使用poetry
poetry add requests
poetry lock  # 生成poetry.lock
```

#### requirements.txt结构
**最佳实践**:
```txt
# requirements.txt
# 生产依赖
requests==2.31.0
fastapi==0.109.0
pydantic==2.5.3

# requirements-dev.txt
# 开发依赖
-r requirements.txt
pytest==7.4.3
black==23.12.1
mypy==1.8.0
```

### 8. 性能优化

#### 字符串拼接
**问题**: 使用+拼接大量字符串
**风险等级**: 中

**反模式**:
```python
# ❌ 低效
result = ""
for item in items:
    result += str(item)  # O(n²)复杂度
```

**最佳实践**:
```python
# ✅ 使用join
result = "".join(str(item) for item in items)  # O(n)复杂度

# ✅ 使用StringIO(流式构建)
from io import StringIO

buffer = StringIO()
for item in items:
    buffer.write(str(item))
result = buffer.getvalue()
```

#### 使用生成器
**问题**: 不必要地构建列表
**风险等级**: 中

**反模式**:
```python
# ❌ 构建完整列表
def get_user_emails(users):
    emails = []
    for user in users:
        if user.is_active:
            emails.append(user.email)
    return emails

# ❌ 不必要的列表
sum([x * 2 for x in range(1000000)])  # 构建临时列表
```

**最佳实践**:
```python
# ✅ 使用生成器
def get_user_emails(users):
    for user in users:
        if user.is_active:
            yield user.email

# ✅ 使用生成器表达式
sum(x * 2 for x in range(1000000))  # 不构建列表
```

### 9. 安全性

#### eval和exec使用
**问题**: 使用eval/exec处理用户输入
**风险等级**: 严重

**反模式**:
```python
# ❌ 危险: 任意代码执行
result = eval(user_input)

# ❌ 危险
exec(user_code)
```

**最佳实践**:
```python
# ✅ 使用ast.literal_eval(仅字面量)
import ast

result = ast.literal_eval(user_input)  # 仅支持字面量

# ✅ 使用配置解析库
import yaml
config = yaml.safe_load(user_input)
```

#### pickle反序列化
**问题**: 反序列化不受信任的pickle数据
**风险等级**: 严重

**反模式**:
```python
# ❌ 危险: 可能任意代码执行
import pickle
data = pickle.loads(untrusted_data)
```

**最佳实践**:
```python
# ✅ 使用JSON(安全)
import json
data = json.loads(untrusted_data)

# 或使用HMAC签名验证
import hmac
import pickle

def safe_loads(data, key):
    # 验证签名
    if not verify_signature(data, key):
        raise ValueError("Invalid signature")
    return pickle.loads(data)
```

### 10. 测试

#### pytest使用
**问题**: 缺少测试或测试覆盖率低
**风险等级**: 中

**最佳实践**:
```python
# ✅ 使用pytest
import pytest

from myapp import calculate

def test_calculate_positive_numbers():
    """Test with positive numbers."""
    assert calculate(2, 3) == 5

def test_calculate_negative_numbers():
    """Test with negative numbers."""
    assert calculate(-2, -3) == -5

def test_calculate_raises_exception():
    """Test exception handling."""
    with pytest.raises(TypeError):
        calculate("a", "b")

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_calculate_various_inputs(a, b, expected):
    """Test with various inputs."""
    assert calculate(a, b) == expected
```

#### Mock使用
**最佳实践**:
```python
# ✅ 正确使用mock
from unittest.mock import patch, MagicMock

@patch('myapp.requests.get')
def test_api_call(mock_get):
    """Test API call with mocked requests."""
    mock_get.return_value.json.return_value = {'status': 'ok'}
    result = fetch_api_data()
    assert result == {'status': 'ok'}
    mock_get.assert_called_once_with('https://api.example.com/data')
```

## Python版本特性

### Python 3.8+
```python
# 海象运算符
if (n := len(items)) > 10:
    print(f"Too many items: {n}")

# 位置参数
def func(a, /, b, *, c):
    pass

# typing.TypedDict
class User(TypedDict):
    name: str
    age: int
```

### Python 3.10+
```python
# 联合类型的新语法
def func(x: int | str | None):  # 而不是 Union[int, str, None]
    pass

# Structural Pattern Matching
match status:
    case 200:
        return "OK"
    case 404:
        return "Not Found"
    case _:
        return "Unknown"
```

## 工具推荐

- **代码格式化**: Black, isort
- **代码检查**: Flake8, Pylint, Ruff
- **类型检查**: mypy
- **测试**: pytest, pytest-cov, hypothesis
- **性能分析**: cProfile, py-spy, memory_profiler
- **安全检查**: bandit, safety

## 审查输出模板

```markdown
### [严重/高/中/低] 问题类型

**位置**: `文件路径:行号`

**问题描述**:
简明描述问题

**代码示例**:
\`\`\`python
# ❌ 当前代码
有问题代码
\`\`\`

**改进建议**:
\`\`\`python
# ✅ 建议代码
改进后代码
\`\`\`

**影响**:
- 代码质量: ...
- 性能: ...
- 可维护性: ...

**参考**: PEP编号或相关文档
```

## 参考资源

- [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 484 -- Type Hints](https://peps.python.org/pep-0484/)
- [The Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
- [Effective Python](https://effectivepython.com/)
