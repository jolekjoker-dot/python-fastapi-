"""
第6课：异常处理

学习目标：
- 理解异常的概念
- 掌握 try/except/finally 语法
- 学会捕获特定异常
- 了解自定义异常
"""

# ==================== 基础异常处理 ====================

# try/except - 捕获异常
try:
    result = 10 / 0
except ZeroDivisionError:
    print("错误：不能除以零")

# 捕获异常并获取错误信息
try:
    numbers = [1, 2, 3]
    print(numbers[10])
except IndexError as e:
    print(f"索引错误: {e}")

# ==================== 多个 except ====================

def safe_divide(a, b):
    """安全除法"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("错误：除数不能为零")
        return None
    except TypeError:
        print("错误：参数必须是数字")
        return None

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # None
print(safe_divide(10, "a"))  # None

# ==================== try/except/else/finally ====================

def read_file(filename: str) -> str | None:
    """读取文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return None
    except PermissionError:
        print(f"没有权限读取文件 {filename}")
        return None
    else:
        # 没有异常时执行
        print(f"成功读取文件 {filename}")
        return content
    finally:
        # 无论是否异常都会执行
        print("文件操作完成")

# 测试
content = read_file("不存在的文件.txt")
print(f"内容: {content}")

# ==================== 常见异常类型 ====================

print("\n常见异常类型示例:")

# 1. ValueError - 值错误
try:
    num = int("abc")
except ValueError as e:
    print(f"ValueError: {e}")

# 2. KeyError - 键错误
try:
    d = {"a": 1}
    value = d["b"]
except KeyError as e:
    print(f"KeyError: {e}")

# 3. AttributeError - 属性错误
try:
    s = "hello"
    s.append("world")
except AttributeError as e:
    print(f"AttributeError: {e}")

# 4. TypeError - 类型错误
try:
    result = "hello" + 123
except TypeError as e:
    print(f"TypeError: {e}")

# ==================== 抛出异常 ====================

def validate_age(age: int) -> int:
    """验证年龄"""
    if not isinstance(age, int):
        raise TypeError("年龄必须是整数")
    if age < 0 or age > 150:
        raise ValueError(f"年龄 {age} 不在有效范围内 (0-150)")
    return age

# 测试
try:
    validate_age(25)    # 正常
    validate_age(-5)    # 抛出 ValueError
except ValueError as e:
    print(f"\n验证错误: {e}")

try:
    validate_age("abc")  # 抛出 TypeError
except TypeError as e:
    print(f"类型错误: {e}")

# ==================== 自定义异常 ====================

class InsufficientFundsError(Exception):
    """余额不足异常"""

    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(f"余额不足：余额 {balance}，尝试取出 {amount}")

class BankAccount:
    """银行账户"""

    def __init__(self, balance: float = 0):
        self._balance = balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("取款金额必须大于0")
        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)
        self._balance -= amount
        return self._balance

    @property
    def balance(self) -> float:
        return self._balance

# 测试
account = BankAccount(1000)

try:
    account.withdraw(500)
    print(f"\n取款后余额: {account.balance}")

    account.withdraw(600)  # 抛出 InsufficientFundsError
except InsufficientFundsError as e:
    print(f"错误: {e}")
    print(f"当前余额: {e.balance}，尝试取出: {e.amount}")

# ==================== 实际应用：数据验证 ====================

class ValidationError(Exception):
    """数据验证异常"""

    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

def validate_user_data(data: dict) -> dict:
    """验证用户数据"""
    errors = []

    # 验证名字
    if "name" not in data:
        errors.append(ValidationError("name", "名字是必填项"))
    elif len(data["name"]) < 2:
        errors.append(ValidationError("name", "名字至少2个字符"))

    # 验证年龄
    if "age" not in data:
        errors.append(ValidationError("age", "年龄是必填项"))
    elif not isinstance(data["age"], int) or data["age"] < 0 or data["age"] > 150:
        errors.append(ValidationError("age", "年龄必须是0-150之间的整数"))

    # 验证邮箱
    if "email" in data and "@" not in data["email"]:
        errors.append(ValidationError("email", "邮箱格式不正确"))

    if errors:
        raise ExceptionGroup("数据验证失败", errors)

    return data

# 测试
test_data = {"name": "张", "age": -5, "email": "invalid"}

try:
    validate_user_data(test_data)
except* ValidationError as eg:
    print("\n数据验证错误:")
    for error in eg.exceptions:
        print(f"  - {error.field}: {error.message}")

# ==================== 练习题 ====================
print("\n" + "="*50)
print("练习题：")
print("="*50)

# 练习1: 安全的类型转换
# 编写一个函数 safe_convert(value, target_type)
# 尝试将 value 转换为 target_type
# 转换失败返回默认值

# 在这里写你的代码：
# def safe_convert(value, target_type, default=None):
#     ...

# 练习2: 输入验证
# 编写函数 validate_email(email)
# 检查：包含@，@后面有.，长度大于5
# 不满足条件抛出自定义异常

# 在这里写你的代码：
# class EmailError(Exception):
#     ...
#
# def validate_email(email: str) -> str:
#     ...

# 练习3: 重试机制
# 编写函数 retry(func, max_attempts=3)
# 如果函数执行失败，自动重试指定次数

# 在这里写你的代码：
# def retry(func, max_attempts=3):
#     ...
