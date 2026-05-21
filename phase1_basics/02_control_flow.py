"""
第2课：条件判断和循环

学习目标：
- 掌握 if/elif/else 条件判断
- 掌握 for 循环和 while 循环
- 理解 break 和 continue
- 学会使用 range() 函数
"""

# ==================== 条件判断 ====================
# if/elif/else 用于根据条件执行不同代码

age = 18

if age < 18:
    print("未成年")
elif age == 18:
    print("刚成年")
else:
    print("成年人")

# 比较运算符
# == 等于, != 不等于, > 大于, < 小于
# >= 大于等于, <= 小于等于

x = 10
y = 20

if x > y:
    print(f"{x} 大于 {y}")
elif x < y:
    print(f"{x} 小于 {y}")
else:
    print(f"{x} 等于 {y}")

# 逻辑运算符
# and 与, or 或, not 非

age = 25
has_ticket = True

if age >= 18 and has_ticket:
    print("允许入场")

if age < 12 or age > 60:
    print("享受优惠")

is_weekend = False
if not is_weekend:
    print("今天是工作日")

# ==================== for 循环 ====================
# for 循环用于遍历序列（列表、字符串、range等）

# 遍历列表
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(f"我喜欢{fruit}")

# 遍历字符串
for char in "Python":
    print(char, end=" ")
print()  # 换行

# 使用 range() 生成数字序列
# range(stop) - 从0到stop-1
# range(start, stop) - 从start到stop-1
# range(start, stop, step) - 从start到stop-1，步长为step

print("\nrange(5):")
for i in range(5):
    print(i, end=" ")  # 0 1 2 3 4
print()

print("\nrange(1, 6):")
for i in range(1, 6):
    print(i, end=" ")  # 1 2 3 4 5
print()

print("\nrange(0, 10, 2):")
for i in range(0, 10, 2):
    print(i, end=" ")  # 0 2 4 6 8
print()

# enumerate() - 同时获取索引和值
print("\n使用 enumerate:")
fruits = ["苹果", "香蕉", "橙子"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# ==================== while 循环 ====================
# while 循环在条件为真时持续执行

count = 0
while count < 5:
    print(f"计数: {count}")
    count += 1  # 等同于 count = count + 1

# 无限循环（需要 break 退出）
print("\nwhile True 示例:")
while True:
    user_input = "quit"  # 模拟用户输入
    if user_input == "quit":
        print("退出循环")
        break  # 跳出循环

# ==================== break 和 continue ====================

# break - 立即退出循环
print("\nbreak 示例:")
for i in range(10):
    if i == 5:
        print("遇到 5，退出循环")
        break
    print(i, end=" ")
print()

# continue - 跳过当前迭代，继续下一次
print("\ncontinue 示例 (跳过偶数):")
for i in range(10):
    if i % 2 == 0:
        continue  # 跳过偶数
    print(i, end=" ")
print()

# ==================== 循环中的 else ====================
# Python 特有：循环正常结束时执行 else
print("\nfor-else 示例:")
for i in range(5):
    print(i, end=" ")
else:
    print("\n循环正常结束")

print("\nfor-else with break:")
for i in range(5):
    if i == 3:
        break
    print(i, end=" ")
else:
    print("这行不会执行，因为循环被 break 中断")

# ==================== 嵌套循环 ====================
print("\n九九乘法表:")
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}x{i}={i*j}", end="\t")
    print()  # 换行

# ==================== 列表推导式 ====================
# 一种简洁的创建列表的方式

# 传统方式
squares = []
for x in range(10):
    squares.append(x ** 2)
print(f"\n传统方式: {squares}")

# 列表推导式
squares = [x ** 2 for x in range(10)]
print(f"列表推导式: {squares}")

# 带条件的列表推导式
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
print(f"偶数的平方: {even_squares}")

# ==================== 练习题 ====================
print("\n" + "="*50)
print("练习题：")
print("="*50)

# 练习1: 判断成绩等级
# 请编写程序，根据分数打印等级：
# 90-100: 优秀
# 80-89: 良好
# 70-79: 中等
# 60-69: 及格
# 0-59: 不及格

# 在这里写你的代码：
# score = 85
# if ...

# 练习2: 计算累加和
# 使用循环计算 1+2+3+...+100 的结果

# 在这里写你的代码：
# total = 0
# for i in ...

# 练习3: 找出偶数
# 使用列表推导式，创建一个列表，包含 1-20 中所有偶数

# 在这里写你的代码：
# even_numbers = [...]

# 练习4: 打印三角形
# 使用嵌套循环打印以下图形：
# *
# **
# ***
# ****
# *****

# 在这里写你的代码：
# for i in range(1, 6):
#     ...
