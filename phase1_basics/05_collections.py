"""
第5课：列表、字典、集合

学习目标：
- 掌握列表（list）的操作
- 掌握字典（dict）的操作
- 了解集合（set）的特性
- 学会列表推导式和字典推导式
"""

# ==================== 列表（List）====================
# 有序、可变、可重复的集合

# 创建列表
fruits = ["苹果", "香蕉", "橙子", "苹果"]  # 可以有重复
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]  # 可以混合类型

# 访问元素
print(f"第一个: {fruits[0]}")     # 苹果
print(f"最后一个: {fruits[-1]}")  # 苹果
print(f"切片: {fruits[1:3]}")     # ['香蕉', '橙子']

# 修改元素
fruits[0] = "草莓"
print(f"修改后: {fruits}")

# 常用方法
fruits = ["苹果", "香蕉", "橙子"]

fruits.append("葡萄")       # 末尾添加
print(f"append: {fruits}")

fruits.insert(1, "芒果")    # 指定位置插入
print(f"insert: {fruits}")

fruits.remove("香蕉")       # 删除第一个匹配项
print(f"remove: {fruits}")

popped = fruits.pop()       # 弹出最后一个
print(f"pop: {popped}, 剩余: {fruits}")

fruits.sort()               # 排序（原地）
print(f"sort: {fruits}")

fruits.reverse()            # 反转（原地）
print(f"reverse: {fruits}")

# 列表长度
print(f"长度: {len(fruits)}")

# 检查元素是否存在
print(f"苹果在列表中: {'苹果' in fruits}")
print(f"西瓜在列表中: {'西瓜' in fruits}")

# 遍历列表
print("\n遍历列表:")
for fruit in fruits:
    print(f"  - {fruit}")

# 带索引遍历
print("\n带索引遍历:")
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")

# ==================== 列表推导式 ====================

# 基本语法: [表达式 for 变量 in 可迭代对象]
squares = [x ** 2 for x in range(1, 6)]
print(f"\n平方数: {squares}")  # [1, 4, 9, 16, 25]

# 带条件: [表达式 for 变量 in 可迭代对象 if 条件]
even_squares = [x ** 2 for x in range(1, 11) if x % 2 == 0]
print(f"偶数平方: {even_squares}")  # [4, 16, 36, 64, 100]

# 实际应用
names = ["张三", "李四", "王五", "赵六"]
short_names = [name for name in names if len(name) <= 2]
print(f"短名字: {short_names}")

# ==================== 字典（Dict）====================
# 无序（Python 3.7+ 有序）、可变、键值对集合

# 创建字典
person = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}

# 也可以用 dict() 构造
person2 = dict(name="李四", age=30, city="上海")

# 访问值
print(f"\n名字: {person['name']}")
print(f"年龄: {person.get('age')}")           # 推荐使用 get
print(f"职业: {person.get('job', '未知')}")    # 不存在时返回默认值

# 修改和添加
person["age"] = 26               # 修改
person["email"] = "zhang@..."   # 添加
print(f"更新后: {person}")

# 删除
del person["email"]              # 使用 del
job = person.pop("job", None)    # 使用 pop（不存在返回默认值）
print(f"删除后: {person}")

# 常用方法
print(f"\n所有键: {list(person.keys())}")
print(f"所有值: {list(person.values())}")
print(f"所有键值对: {list(person.items())}")

# 遍历字典
print("\n遍历字典:")
for key, value in person.items():
    print(f"  {key}: {value}")

# 检查键是否存在
print(f"\n'name' in person: {'name' in person}")
print(f"'job' in person: {'job' in person}")

# ==================== 字典推导式 ====================

# 基本语法: {键表达式: 值表达式 for 变量 in 可迭代对象}
squares_dict = {x: x ** 2 for x in range(1, 6)}
print(f"\n平方字典: {squares_dict}")

# 带条件
even_dict = {x: x ** 2 for x in range(1, 11) if x % 2 == 0}
print(f"偶数字典: {even_dict}")

# 实际应用：反转字典
original = {"a": 1, "b": 2, "c": 3}
reversed_dict = {v: k for k, v in original.items()}
print(f"反转字典: {reversed_dict}")

# ==================== 嵌套结构 ====================

# 列表中嵌套字典
students = [
    {"name": "张三", "scores": [85, 90, 78]},
    {"name": "李四", "scores": [92, 88, 95]},
    {"name": "王五", "scores": [78, 85, 82]},
]

# 计算每个学生的平均分
print("\n学生平均分:")
for student in students:
    avg = sum(student["scores"]) / len(student["scores"])
    print(f"  {student['name']}: {avg:.1f}")

# 字典中嵌套列表
school = {
    "name": "Python大学",
    "departments": ["计算机", "数学", "物理"],
    "students": {
        "计算机": 500,
        "数学": 300,
        "物理": 200
    }
}

print(f"\n学校: {school['name']}")
print(f"院系: {', '.join(school['departments'])}")

# ==================== 集合（Set）====================
# 无序、可变、不可重复的集合

# 创建集合
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

# 添加和删除
set1.add(6)
print(f"\n添加后: {set1}")

set1.discard(6)  # 删除（不存在不报错）
print(f"删除后: {set1}")

# 集合运算
print(f"\n并集: {set1 | set2}")      # {1, 2, 3, 4, 5, 6, 7, 8}
print(f"交集: {set1 & set2}")        # {4, 5}
print(f"差集: {set1 - set2}")        # {1, 2, 3}
print(f"对称差集: {set1 ^ set2}")    # {1, 2, 3, 6, 7, 8}

# 集合去重
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_numbers = list(set(numbers))
print(f"\n去重: {unique_numbers}")

# ==================== 练习题 ====================
print("\n" + "="*50)
print("练习题：")
print("="*50)

# 练习1: 列表操作
# 创建一个列表 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 使用列表推导式获取所有偶数的平方

# 在这里写你的代码：
# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# result = [...]

# 练习2: 字典操作
# 创建一个字典存储学生成绩
# 计算平均分并找出最高分的学生

# 在这里写你的代码：
# grades = {
#     "张三": [85, 90, 78],
#     "李四": [92, 88, 95],
#     "王五": [78, 85, 82],
# }

# 练习3: 集合操作
# 两个班的学生名单，找出：
# 1. 两个班都有的学生
# 2. 只在A班的学生
# 3. 所有学生（去重）

# 在这里写你的代码：
# class_a = {"张三", "李四", "王五", "赵六"}
# class_b = {"李四", "王五", "孙七", "周八"}
