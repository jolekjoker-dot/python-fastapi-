"""
第3课：函数定义和使用

学习目标：
- 掌握函数定义语法
- 理解参数传递（位置参数、关键字参数、默认参数）
- 理解返回值
- 了解可变参数 *args 和 **kwargs
"""

# ==================== 函数基础 ====================
# 使用 def 关键字定义函数

def greet():
    """这是一个简单的函数（文档字符串）"""
    print("你好，世界！")

# 调用函数
greet()

# ==================== 带参数的函数 ====================

def greet_name(name):
    """向指定的人打招呼"""
    print(f"你好，{name}！")

greet_name("张三")  # 输出: 你好，张三！
greet_name("李四")  # 输出: 你好，李四！

# 多个参数
def introduce(name, age):
    """自我介绍"""
    print(f"我叫{name}，今年{age}岁")

introduce("张三", 25)  # 位置参数

# ==================== 参数类型 ====================

# 1. 位置参数 - 按顺序传递
def add(a, b):
    return a + b

result = add(3, 5)  # a=3, b=5
print(f"3 + 5 = {result}")

# 2. 关键字参数 - 按名称传递
result = add(b=5, a=3)  # 顺序可以不同
print(f"3 + 5 = {result}")

# 3. 默认参数 - 有默认值的参数
def greet_with_title(name, title="同学"):
    print(f"你好，{name}{title}！")

greet_with_title("张三")           # 使用默认值
greet_with_title("张三", "老师")   # 覆盖默认值

# 4. 混合使用
def create_user(name, age, role="user", active=True):
    return {
        "name": name,
        "age": age,
        "role": role,
        "active": active
    }

user1 = create_user("张三", 25)  # 使用默认值
user2 = create_user("李四", 30, role="admin")  # 部分覆盖
print(f"用户1: {user1}")
print(f"用户2: {user2}")

# ==================== 返回值 ====================

# 返回单个值
def square(x):
    return x ** 2

result = square(5)
print(f"5的平方 = {result}")

# 返回多个值（实际返回元组）
def min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = min_max([3, 1, 4, 1, 5, 9])
print(f"最小值: {minimum}, 最大值: {maximum}")

# 没有 return 语句，返回 None
def say_hello(name):
    print(f"你好，{name}！")
    # 没有 return

result = say_hello("张三")
print(f"返回值: {result}")  # None

# ==================== 可变参数 ====================

# *args - 接收任意数量的位置参数（元组）
def sum_all(*args):
    print(f"参数: {args}")
    print(f"类型: {type(args)}")
    return sum(args)

result = sum_all(1, 2, 3, 4, 5)
print(f"总和: {result}")

# **kwargs - 接收任意数量的关键字参数（字典）
def print_info(**kwargs):
    print(f"参数: {kwargs}")
    print(f"类型: {type(kwargs)}")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_info(name="张三", age=25, city="北京")

# 混合使用
def func(a, b, *args, **kwargs):
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"args = {args}")
    print(f"kwargs = {kwargs}")

func(1, 2, 3, 4, x=5, y=6)

# ==================== Lambda 函数 ====================
# 简短的匿名函数

# 普通函数
def double(x):
    return x * 2

# Lambda 函数
double_lambda = lambda x: x * 2

print(f"double(5) = {double(5)}")
print(f"double_lambda(5) = {double_lambda(5)}")

# Lambda 常用于排序
students = [
    {"name": "张三", "age": 25},
    {"name": "李四", "age": 20},
    {"name": "王五", "age": 22},
]

# 按年龄排序
students_sorted = sorted(students, key=lambda s: s["age"])
print("\n按年龄排序:")
for s in students_sorted:
    print(f"  {s['name']}: {s['age']}")

# ==================== 函数作为参数 ====================

def apply_operation(x, y, operation):
    """将操作应用于两个数"""
    return operation(x, y)

def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

print(f"\nadd(3, 5) = {apply_operation(3, 5, add)}")
print(f"multiply(3, 5) = {apply_operation(3, 5, multiply)}")

# ==================== 作用域 ====================

# 全局变量
global_var = "我是全局变量"

def test_scope():
    # 局部变量
    local_var = "我是局部变量"
    print(global_var)   # 可以读取全局变量
    print(local_var)    # 可以读取局部变量

test_scope()
print(global_var)
# print(local_var)  # 错误！局部变量在函数外不可访问

# 修改全局变量需要使用 global 关键字
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(f"\ncounter = {counter}")  # 2

# ==================== 练习题 ====================
print("\n" + "="*50)
print("练习题：")
print("="*50)

# 练习1: 编写计算器函数
# 创建一个函数 calculate(a, b, operator)
# operator 可以是 "+", "-", "*", "/"
# 返回计算结果

# 在这里写你的代码：
# def calculate(a, b, operator):
#     ...

# 练习2: 编写成绩等级函数
# 创建一个函数 get_grade(score)
# 返回等级：A(90-100), B(80-89), C(70-79), D(60-69), F(0-59)

# 在这里写你的代码：
# def get_grade(score):
#     ...

# 练习3: 编写列表处理函数
# 创建一个函数 filter_even(numbers)
# 接收一个数字列表，返回其中的偶数列表

# 在这里写你的代码：
# def filter_even(numbers):
#     ...
