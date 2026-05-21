"""
第1课：变量和数据类型

学习目标：
- 理解 Python 中的变量概念
- 掌握基本数据类型：int, str, float, bool
- 学会类型转换
- 理解动态类型特性
"""

# ==================== 变量基础 ====================
# Python 是动态类型语言，不需要声明变量类型
# 直接赋值即可创建变量

# 整数 (int)
age = 25
print(f"年龄: {age}")  # 输出: 年龄: 25
print(f"年龄的类型: {type(age)}")  # 输出: <class 'int'>

# 字符串 (str)
name = "张三"
greeting = '你好'  # 单引号和双引号都可以
message = f"欢迎, {name}!"  # f-string 格式化
print(message)  # 输出: 欢迎, 张三!

# 浮点数 (float)
height = 175.5
price = 99.99
print(f"身高: {height}cm")  # 输出: 身高: 175.5cm

# 布尔值 (bool)
is_student = True
is_working = False
print(f"是学生: {is_student}")  # 输出: 是学生: True

# ==================== 类型转换 ====================
# 不同类型之间可以相互转换

# 字符串转整数
age_str = "25"
age_int = int(age_str)  # 转换为整数
print(f"字符串 '{age_str}' 转整数: {age_int}")

# 整数转字符串
number = 100
number_str = str(number)  # 转换为字符串
print(f"整数 {number} 转字符串: '{number_str}'")

# 字符串转浮点数
price_str = "99.99"
price_float = float(price_str)
print(f"字符串 '{price_str}' 转浮点数: {price_float}")

# 布尔值转换
# 以下值会被转换为 False: 0, 0.0, "", None, [], {}, ()
# 其他值转换为 True
print(f"int(True) = {int(True)}")   # 1
print(f"int(False) = {int(False)}")  # 0
print(f"bool(0) = {bool(0)}")       # False
print(f"bool(1) = {bool(1)}")       # True
print(f"bool('') = {bool('')}")     # False
print(f"bool('hello') = {bool('hello')}")  # True

# ==================== 字符串操作 ====================
text = "Hello, Python!"

# 字符串长度
print(f"长度: {len(text)}")  # 14

# 大小写转换
print(f"大写: {text.upper()}")
print(f"小写: {text.lower()}")

# 查找子字符串
print(f"Python 的位置: {text.find('Python')}")  # 7

# 替换
new_text = text.replace("Python", "World")
print(f"替换后: {new_text}")

# 切片（获取子字符串）
print(f"前5个字符: {text[:5]}")  # Hello
print(f"后6个字符: {text[-6:]}")  # ython!

# ==================== 数学运算 ====================
a = 10
b = 3

print(f"{a} + {b} = {a + b}")    # 加法: 13
print(f"{a} - {b} = {a - b}")    # 减法: 7
print(f"{a} * {b} = {a * b}")    # 乘法: 30
print(f"{a} / {b} = {a / b}")    # 除法: 3.333...
print(f"{a} // {b} = {a // b}")  # 整除: 3
print(f"{a} % {b} = {a % b}")    # 取余: 1
print(f"{a} ** {b} = {a ** b}")  # 幂运算: 1000

# ==================== 练习题 ====================
print("\n" + "="*50)
print("练习题：")
print("="*50)

# 练习1: 创建变量并打印
# 请创建以下变量并打印它们：
# - 你的名字 (字符串)
# - 你的年龄 (整数)
# - 你的身高 (浮点数)
# - 你是否是学生 (布尔值)

# 在这里写你的代码：
# my_name = "..."
# my_age = ...
# my_height = ...
# my_is_student = ...

# 练习2: 类型转换
# 将字符串 "3.14" 转换为浮点数并打印
# 将整数 2024 转换为字符串并拼接 "年"

# 练习3: 字符串操作
# 给定字符串 "fastapi is awesome"
# 1. 打印它的长度
# 2. 将它转换为大写
# 3. 将 "awesome" 替换为 "great"
