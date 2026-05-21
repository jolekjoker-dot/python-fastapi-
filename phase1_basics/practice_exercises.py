"""
第一阶段综合练习题

完成以下练习，检验你的 Python 基础掌握程度。
每个练习都有详细的要求和提示。
"""

# ==================== 练习1：学生管理系统 ====================
# 创建一个简单的学生管理系统

class Student:
    """学生类"""

    def __init__(self, student_id: int, name: str, age: int, scores: list[float]):
        """
        初始化学生

        Args:
            student_id: 学号
            name: 姓名
            age: 年龄
            scores: 成绩列表
        """
        # TODO: 初始化属性
        pass

    def average_score(self) -> float:
        """计算平均分"""
        # TODO: 实现计算平均分
        pass

    def is_passed(self) -> bool:
        """判断是否及格（平均分>=60）"""
        # TODO: 实现判断
        pass

    def __str__(self) -> str:
        """返回学生信息字符串"""
        # TODO: 实现字符串表示
        pass


class StudentManager:
    """学生管理器"""

    def __init__(self):
        """初始化"""
        # TODO: 初始化学生列表
        pass

    def add_student(self, student: Student) -> bool:
        """添加学生"""
        # TODO: 实现添加学生
        # 检查学号是否已存在
        pass

    def find_by_id(self, student_id: int) -> Student | None:
        """根据学号查找学生"""
        # TODO: 实现查找
        pass

    def get_top_students(self, n: int = 3) -> list[Student]:
        """获取成绩前n名的学生"""
        # TODO: 实现排序和切片
        pass

    def get_average_score(self) -> float:
        """获取所有学生的平均分"""
        # TODO: 实现计算
        pass


# 测试代码
def test_student_system():
    """测试学生管理系统"""
    print("=== 测试学生管理系统 ===")

    manager = StudentManager()

    # 添加学生
    students_data = [
        (1, "张三", 20, [85, 90, 78]),
        (2, "李四", 21, [92, 88, 95]),
        (3, "王五", 19, [78, 85, 82]),
        (4, "赵六", 22, [65, 70, 72]),
    ]

    for sid, name, age, scores in students_data:
        student = Student(sid, name, age, scores)
        manager.add_student(student)

    # 测试查找
    student = manager.find_by_id(1)
    if student:
        print(f"找到学生: {student}")
        print(f"平均分: {student.average_score():.1f}")
        print(f"是否及格: {student.is_passed()}")

    # 测试排序
    top_students = manager.get_top_students(2)
    print("\n前2名学生:")
    for s in top_students:
        print(f"  {s.name}: {s.average_score():.1f}")

    # 测试平均分
    avg = manager.get_average_score()
    print(f"\n全班平均分: {avg:.1f}")


# ==================== 练习2：待办事项列表 ====================
# 创建一个待办事项管理程序

class TodoItem:
    """待办事项类"""

    def __init__(self, title: str, description: str = "", priority: str = "medium"):
        """
        初始化待办事项

        Args:
            title: 标题
            description: 描述
            priority: 优先级 (low/medium/high)
        """
        # TODO: 初始化属性，包括 id, title, description, priority, completed, created_at
        pass

    def mark_completed(self):
        """标记为已完成"""
        # TODO: 实现
        pass

    def __str__(self) -> str:
        """返回待办事项字符串"""
        # TODO: 实现，包含完成状态标记
        pass


class TodoList:
    """待办事项列表"""

    def __init__(self):
        """初始化"""
        # TODO: 初始化列表和ID计数器
        pass

    def add(self, title: str, description: str = "", priority: str = "medium") -> TodoItem:
        """添加待办事项"""
        # TODO: 实现添加，返回创建的项目
        pass

    def complete(self, todo_id: int) -> bool:
        """标记完成"""
        # TODO: 实现标记完成
        pass

    def remove(self, todo_id: int) -> bool:
        """删除待办事项"""
        # TODO: 实现删除
        pass

    def get_all(self, completed: bool | None = None) -> list[TodoItem]:
        """获取待办事项列表"""
        # TODO: 实现过滤
        # completed=None: 返回所有
        # completed=True: 只返回已完成
        # completed=False: 只返回未完成
        pass

    def get_by_priority(self, priority: str) -> list[TodoItem]:
        """按优先级获取"""
        # TODO: 实现按优先级过滤
        pass


# 测试代码
def test_todo_list():
    """测试待办事项列表"""
    print("\n=== 测试待办事项列表 ===")

    todo_list = TodoList()

    # 添加待办事项
    todo_list.add("学习 Python", "完成基础教程", "high")
    todo_list.add("写代码", "练习 FastAPI", "medium")
    todo_list.add("看电影", priority="low")

    # 获取所有待办
    all_todos = todo_list.get_all()
    print("所有待办:")
    for todo in all_todos:
        print(f"  {todo}")

    # 标记完成
    todo_list.complete(1)

    # 获取未完成
    pending = todo_list.get_all(completed=False)
    print(f"\n未完成: {len(pending)}项")

    # 获取高优先级
    high_priority = todo_list.get_by_priority("high")
    print(f"高优先级: {len(high_priority)}项")


# ==================== 练习3：数据处理工具 ====================
# 创建数据处理工具函数

def calculate_statistics(numbers: list[float]) -> dict:
    """
    计算统计数据

    Args:
        numbers: 数字列表

    Returns:
        包含 count, sum, average, min, max, range 的字典
    """
    # TODO: 实现统计计算
    pass


def filter_outliers(numbers: list[float], threshold: float = 2.0) -> list[float]:
    """
    过滤异常值（超过 threshold 个标准差）

    Args:
        numbers: 数字列表
        threshold: 标准差倍数阈值

    Returns:
        过滤后的列表
    """
    # TODO: 实现异常值过滤
    pass


def group_by_key(items: list[dict], key: str) -> dict[list]:
    """
    按键分组

    Args:
        items: 字典列表
        key: 分组键

    Returns:
        分组后的字典
    """
    # TODO: 实现分组
    pass


# 测试代码
def test_data_processing():
    """测试数据处理工具"""
    print("\n=== 测试数据处理工具 ===")

    numbers = [10, 20, 30, 40, 50, 100, 200, 500]
    stats = calculate_statistics(numbers)
    print(f"统计数据: {stats}")

    # 过滤异常值
    filtered = filter_outliers(numbers, threshold=1.5)
    print(f"过滤后: {filtered}")

    # 分组测试
    students = [
        {"name": "张三", "grade": "A"},
        {"name": "李四", "grade": "B"},
        {"name": "王五", "grade": "A"},
        {"name": "赵六", "grade": "B"},
        {"name": "钱七", "grade": "A"},
    ]
    grouped = group_by_key(students, "grade")
    print(f"按等级分组: {grouped}")


# ==================== 练习4：文件处理 ====================
# 创建文件处理工具

def read_csv(filename: str) -> list[dict]:
    """
    读取 CSV 文件

    Args:
        filename: 文件名

    Returns:
        字典列表
    """
    # TODO: 实现 CSV 读取
    # 提示：使用 open() 和 split()
    pass


def write_csv(filename: str, data: list[dict]) -> bool:
    """
    写入 CSV 文件

    Args:
        filename: 文件名
        data: 字典列表

    Returns:
        是否成功
    """
    # TODO: 实现 CSV 写入
    pass


def merge_csv_files(file1: str, file2: str, output: str) -> bool:
    """
    合并两个 CSV 文件

    Args:
        file1: 第一个文件
        file2: 第二个文件
        output: 输出文件

    Returns:
        是否成功
    """
    # TODO: 实现合并
    pass


# ==================== 主程序 ====================

if __name__ == "__main__":
    print("第一阶段综合练习")
    print("=" * 50)

    # 取消注释来测试各个练习
    # test_student_system()
    # test_todo_list()
    # test_data_processing()

    print("\n请完成上述练习，检验你的 Python 基础！")
    print("完成后，可以进入第二阶段学习 FastAPI。")
