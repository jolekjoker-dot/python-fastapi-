"""
内存数据存储

模拟数据库操作，使用字典存储数据
后续可以替换为真实的数据库操作
"""

from datetime import datetime
from models import TodoCreate, TodoUpdate, TodoInDB, TodoStatus, Priority


class MemoryStore:
    """内存数据存储类"""

    def __init__(self):
        """初始化存储"""
        self._todos: dict[int, TodoInDB] = {}
        self._next_id: int = 1
        self._init_sample_data()

    def _init_sample_data(self):
        """初始化示例数据"""
        sample_todos = [
            TodoCreate(
                title="学习 Python 基础",
                description="完成 Python 基础教程",
                priority=Priority.HIGH,
                due_date=datetime(2024, 12, 31),
            ),
            TodoCreate(
                title="学习 FastAPI",
                description="完成 FastAPI 核心教程",
                priority=Priority.HIGH,
            ),
            TodoCreate(
                title="写项目文档",
                description="为项目编写 README 和 API 文档",
                priority=Priority.MEDIUM,
            ),
            TodoCreate(
                title="代码审查",
                description="审查团队成员的代码",
                priority=Priority.LOW,
            ),
        ]

        for todo in sample_todos:
            self.create(todo)

    def create(self, todo: TodoCreate) -> TodoInDB:
        """创建待办事项"""
        now = datetime.now()
        db_todo = TodoInDB(
            id=self._next_id,
            created_at=now,
            updated_at=now,
            **todo.model_dump(),
        )
        self._todos[self._next_id] = db_todo
        self._next_id += 1
        return db_todo

    def get_all(
        self,
        status: TodoStatus | None = None,
        priority: Priority | None = None,
    ) -> list[TodoInDB]:
        """获取所有待办事项（支持过滤）"""
        todos = [
            todo for todo in self._todos.values()
            if not todo.is_deleted
        ]

        if status:
            todos = [t for t in todos if t.status == status]
        if priority:
            todos = [t for t in todos if t.priority == priority]

        # 按创建时间倒序排列
        return sorted(todos, key=lambda t: t.created_at, reverse=True)

    def get_by_id(self, todo_id: int) -> TodoInDB | None:
        """根据 ID 获取待办事项"""
        todo = self._todos.get(todo_id)
        if todo and not todo.is_deleted:
            return todo
        return None

    def update(self, todo_id: int, todo_update: TodoUpdate) -> TodoInDB | None:
        """更新待办事项"""
        todo = self.get_by_id(todo_id)
        if not todo:
            return None

        # 获取更新数据，排除未设置的字段
        update_data = todo_update.model_dump(exclude_unset=True)

        # 更新字段
        for field, value in update_data.items():
            setattr(todo, field, value)

        # 更新时间
        todo.updated_at = datetime.now()

        return todo

    def delete(self, todo_id: int) -> bool:
        """删除待办事项（软删除）"""
        todo = self.get_by_id(todo_id)
        if not todo:
            return False

        todo.is_deleted = True
        todo.updated_at = datetime.now()
        return True

    def complete(self, todo_id: int) -> TodoInDB | None:
        """标记为完成"""
        todo = self.get_by_id(todo_id)
        if not todo:
            return None

        todo.status = TodoStatus.COMPLETED
        todo.updated_at = datetime.now()
        return todo

    def get_stats(self) -> dict:
        """获取统计信息"""
        active_todos = [t for t in self._todos.values() if not t.is_deleted]
        return {
            "total": len(active_todos),
            "pending": len([t for t in active_todos if t.status == TodoStatus.PENDING]),
            "in_progress": len([t for t in active_todos if t.status == TodoStatus.IN_PROGRESS]),
            "completed": len([t for t in active_todos if t.status == TodoStatus.COMPLETED]),
        }


# 创建全局存储实例
# 后续可以替换为数据库连接
todo_store = MemoryStore()
