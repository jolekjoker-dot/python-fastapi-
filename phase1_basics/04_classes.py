"""
第4课：类和面向对象编程

学习目标：
- 理解类和对象的概念
- 掌握 __init__ 构造方法
- 理解 self 的作用
- 学会定义方法
- 了解继承
"""

# ==================== 类的基础 ====================
# 类是对象的蓝图/模板
# 对象是类的实例

class Dog:
    """狗类"""

    def __init__(self, name: str, age: int):
        """
        构造方法，创建对象时自动调用
        self 代表对象本身
        """
        self.name = name  # 实例属性
        self.age = age

    def bark(self):
        """实例方法"""
        return f"{self.name}说：汪汪！"

    def introduce(self):
        """自我介绍"""
        return f"我叫{self.name}，今年{self.age}岁"

# 创建对象（实例化）
dog1 = Dog("旺财", 3)
dog2 = Dog("小白", 2)

# 访问属性和方法
print(dog1.name)         # 旺财
print(dog1.bark())       # 旺财说：汪汪！
print(dog2.introduce())  # 我叫小白，今年2岁

# ==================== 类属性和实例属性 ====================

class Student:
    """学生类"""

    # 类属性 - 所有实例共享
    school = "Python大学"
    student_count = 0

    def __init__(self, name: str, grade: int):
        # 实例属性 - 每个实例独有
        self.name = name
        self.grade = grade
        Student.student_count += 1  # 修改类属性

    def info(self):
        return f"{self.name} - {self.school} - {self.grade}年级"

# 创建实例
s1 = Student("张三", 1)
s2 = Student("李四", 2)

print(s1.info())  # 张三 - Python大学 - 1年级
print(s2.info())  # 李四 - Python大学 - 2年级
print(f"学生总数: {Student.student_count}")  # 2

# ==================== 方法类型 ====================

class Calculator:
    """计算器类"""

    def __init__(self):
        self.history = []

    # 实例方法 - 操作实例数据
    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    # 类方法 - 操作类属性
    @classmethod
    def create_scientific(cls):
        """工厂方法，创建科学计算器"""
        print("创建科学计算器")
        return cls()

    # 静态方法 - 与类相关但不需要访问类或实例
    @staticmethod
    def is_number(value) -> bool:
        """检查是否为数字"""
        try:
            float(value)
            return True
        except ValueError:
            return False

# 使用
calc = Calculator()
print(calc.add(3, 5))       # 8
print(calc.subtract(10, 3)) # 7
print(f"历史记录: {calc.history}")

# 类方法
calc2 = Calculator.create_scientific()

# 静态方法
print(Calculator.is_number("123"))   # True
print(Calculator.is_number("abc"))   # False

# ==================== 继承 ====================
# 继承允许创建一个类基于另一个类

class Animal:
    """动物基类"""

    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species

    def speak(self):
        return f"{self.name}发出声音"

    def info(self):
        return f"{self.name}是一只{self.species}"

class Cat(Animal):
    """猫类，继承自动物类"""

    def __init__(self, name: str, color: str):
        super().__init__(name, "猫")  # 调用父类构造方法
        self.color = color

    def speak(self):
        """重写父类方法"""
        return f"{self.name}说：喵~"

    def purr(self):
        """猫特有的方法"""
        return f"{self.name}在打呼噜"

class Dog2(Animal):
    """狗类，继承自动物类"""

    def __init__(self, name: str, breed: str):
        super().__init__(name, "狗")
        self.breed = breed

    def speak(self):
        return f"{self.name}说：汪汪！"

    def fetch(self):
        return f"{self.name}去捡球了"

# 使用继承
cat = Cat("小花", "橘色")
dog = Dog2("旺财", "金毛")

print(cat.info())    # 小花是一只猫
print(cat.speak())   # 小花说：喵~
print(cat.purr())    # 小花在打呼噜

print(dog.info())    # 旺财是一只狗
print(dog.speak())   # 旺财说：汪汪！
print(dog.fetch())   # 旺财去捡球了

# ==================== 魔术方法 ====================
# 以双下划线开头和结尾的特殊方法

class Point:
    """点类，演示魔术方法"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        """定义 print() 输出的内容"""
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        """定义在解释器中的显示"""
        return f"Point(x={self.x}, y={self.y})"

    def __eq__(self, other):
        """定义 == 比较"""
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        """定义 + 运算"""
        return Point(self.x + other.x, self.y + other.y)

    def __len__(self):
        """定义 len() 函数"""
        return int((self.x ** 2 + self.y ** 2) ** 0.5)

p1 = Point(1, 2)
p2 = Point(3, 4)

print(p1)              # Point(1, 2)
print(repr(p2))        # Point(x=3, y=4)
print(p1 == Point(1, 2))  # True
print(p1 + p2)         # Point(4, 6)
print(len(p1))         # 2

# ==================== 封装 ====================
# 使用下划线约定表示私有属性/方法

class BankAccount:
    """银行账户类"""

    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner      # 公开属性
        self._balance = balance  # 受保护属性（约定）
        self.__pin = "1234"     # 私有属性（名称修饰）

    def deposit(self, amount: float):
        """存款"""
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """取款"""
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self) -> float:
        """获取余额（推荐使用方法访问）"""
        return self._balance

account = BankAccount("张三", 1000)
account.deposit(500)
account.withdraw(200)
print(f"余额: {account.get_balance()}")  # 1300

# ==================== 练习题 ====================
print("\n" + "="*50)
print("练习题：")
print("="*50)

# 练习1: 创建矩形类
# 属性: width, height
# 方法: area() 计算面积, perimeter() 计算周长
# 魔术方法: __str__ 返回描述

# 在这里写你的代码：
# class Rectangle:
#     ...

# 练习2: 创建银行账户类
# 属性: owner, balance
# 方法: deposit(amount), withdraw(amount), get_balance()
# 规则: 不能取超过余额的钱

# 在这里写你的代码：
# class BankAccount2:
#     ...

# 练习3: 创建形状继承体系
# 基类: Shape (属性: name, 方法: area(), describe())
# 子类: Circle (属性: radius)
# 子类: Square (属性: side)

# 在这里写你的代码：
# class Shape:
#     ...
