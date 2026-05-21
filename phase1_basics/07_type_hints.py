"""
第7课：类型提示（Type Hints）

学习目标：
- 理解类型提示的作用
- 掌握基本类型的标注
- 学会使用 Optional, List, Dict 等
- 了解 Union 和 Any
"""

# ==================== 为什么需要类型提示 ====================
# 1. 提高代码可读性
# 2. IDE 自动补全和错误检查
# 3. 运行时不会强制检查（Python 仍是动态类型）
# 4. FastAPI 依赖类型提示进行数据校验

# ==================== 基本类型 ====================

# 变量类型标注
name: str = "张三"
age: int = 25
height: float = 175.5
is_student: bool = True

# 函数参数和返回值类型标注
def greet(name: str) -> str:
    """返回问候语"""
    return f"你好，{name}！"

def add(a: int, b: int) -> int:
    """返回两数之和"""
    return a + b

def is_adult(age: int) -> bool:
    """判断是否成年"""
    return age >= 18

# ==================== Optional 类型 ====================
# Optional[X] 等价于 Union[X, None]，表示可以是 X 或 None

from typing import Optional

def find_user(user_id: int) -> Optional[dict]:
    """查找用户，可能返回 None"""
    users = {
        1: {"name": "张三", "age": 25},
        2: {"name": "李四", "age": 30},
    }
    return users.get(user_id)

# 使用示例
user = find_user(1)
if user is not None:
    print(f"找到用户: {user['name']}")
else:
    print("用户不存在")

# ==================== 容器类型 ====================
from typing import List, Dict, Tuple, Set

# List - 列表类型
def get_names() -> List[str]:
    return ["张三", "李四", "王五"]

def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)

# Dict - 字典类型
def get_user() -> Dict[str, any]:
    return {"name": "张三", "age": 25}

def process_data(data: Dict[str, List[int]]) -> Dict[str, int]:
    """处理数据，返回每个键对应列表的和"""
    return {k: sum(v) for k, v in data.items()}

# Tuple - 元组类型
def get_coordinates() -> Tuple[float, float]:
    return (116.4, 39.9)

def get_user_info() -> Tuple[str, int, bool]:
    return ("张三", 25, True)

# Set - 集合类型
def get_unique_tags() -> Set[str]:
    return {"python", "fastapi", "web"}

# ==================== Union 类型 ====================
# Union[X, Y] 表示可以是 X 或 Y

from typing import Union

def process_id(user_id: Union[int, str]) -> str:
    """处理 ID，可以是整数或字符串"""
    return str(user_id)

# Python 3.10+ 可以使用 | 语法
def process_id_new(user_id: int | str) -> str:
    return str(user_id)

# ==================== Any 类型 ====================
from typing import Any

def process_anything(data: Any) -> Any:
    """处理任意类型的数据"""
    return data

# ==================== 类型别名 ====================
from typing import TypeAlias

# 为复杂类型创建别名
UserId: TypeAlias = int
UserData: TypeAlias = Dict[str, Any]
UserList: TypeAlias = List[UserData]

def get_users() -> UserList:
    return [
        {"name": "张三", "age": 25},
        {"name": "李四", "age": 30},
    ]

# ==================== 类型在类中的使用 ====================

class User:
    """用户类，使用类型提示"""

    def __init__(self, name: str, age: int, email: Optional[str] = None):
        self.name: str = name
        self.age: int = age
        self.email: Optional[str] = email
        self.tags: List[str] = []

    def add_tag(self, tag: str) -> None:
        """添加标签"""
        self.tags.append(tag)

    def get_info(self) -> Dict[str, Any]:
        """获取用户信息"""
        return {
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "tags": self.tags,
        }

    def __str__(self) -> str:
        return f"User(name={self.name}, age={self.age})"

# ==================== FastAPI 中的类型提示 ====================
# 这是 FastAPI 的核心特性

from pydantic import BaseModel
from datetime import datetime
from enum import Enum

# 定义枚举
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# 定义 Pydantic 模型（FastAPI 用这个进行数据校验）
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    due_date: Optional[datetime] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: Priority
    completed: bool
    created_at: datetime

# 模拟 FastAPI 路由函数的类型提示
def create_todo(todo: TodoCreate) -> TodoResponse:
    """创建待办事项（模拟）"""
    return TodoResponse(
        id=1,
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        completed=False,
        created_at=datetime.now()
    )

def get_todos(skip: int = 0, limit: int = 10) -> List[TodoResponse]:
    """获取待办列表（模拟）"""
    return []

def get_todo_by_id(todo_id: int) -> Optional[TodoResponse]:
    """获取单个待办（模拟）"""
    return None

# ==================== 类型检查工具 ====================
# 可以使用 mypy 进行静态类型检查
# pip install mypy
# mypy your_file.py

# ==================== 练习题 ====================
print("\n" + "="*50)
print("练习题：")
print("="*50)

# 练习1: 为函数添加类型提示
# def calculate_average(numbers):
#     if not numbers:
#         return 0
#     return sum(numbers) / len(numbers)

# 在这里写你的代码：
# def calculate_average(numbers: ...) -> ...:
#     ...

# 练习2: 定义带类型提示的类
# 创建一个 Book 类，包含：
# - title: str
# - author: str
# - pages: int
# - price: float
# - tags: List[str]
# - rating: Optional[float]

# 在这里写你的代码：
# class Book:
#     ...

# 练习3: 使用 Pydantic 模型
# 创建一个 Student 模型：
# - name: str (必填，2-50字符)
# - age: int (必填，0-150)
# - email: Optional[str]
# - grades: List[float]

# 在这里写你的代码：
# class Student(BaseModel):
#     ...
