"""
数据模型定义

定义待办事项相关的 Pydantic 模型
"""

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# ==================== 枚举类型 ====================

class Priority(str, Enum):
    """优先级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoStatus(str, Enum):
    """状态"""
    PENDING = "pending"      # 待处理
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成


# ==================== 请求模型 ====================

class TodoCreate(BaseModel):
    """创建待办事项的请求模型"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="待办事项标题",
        example="学习 FastAPI",
    )
    description: str | None = Field(
        None,
        max_length=1000,
        description="详细描述",
        example="完成 FastAPI 教程的学习",
    )
    priority: Priority = Field(
        default=Priority.MEDIUM,
        description="优先级",
    )
    due_date: datetime | None = Field(
        None,
        description="截止日期",
    )


class TodoUpdate(BaseModel):
    """更新待办事项的请求模型（所有字段可选）"""
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    priority: Priority | None = None
    status: TodoStatus | None = None
    due_date: datetime | None = None


# ==================== 响应模型 ====================

class TodoResponse(BaseModel):
    """返回给客户端的待办事项模型"""
    id: int
    title: str
    description: str | None
    priority: Priority
    status: TodoStatus
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    is_overdue: bool = False


class TodoListResponse(BaseModel):
    """待办事项列表响应"""
    todos: list[TodoResponse]
    total: int
    pending: int
    in_progress: int
    completed: int


# ==================== 数据库模型 ====================

class TodoInDB(BaseModel):
    """存储在数据库中的待办事项模型"""
    id: int
    title: str
    description: str | None = None
    priority: Priority = Priority.MEDIUM
    status: TodoStatus = TodoStatus.PENDING
    due_date: datetime | None = None
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False

    def to_response(self) -> TodoResponse:
        """转换为响应模型"""
        is_overdue = False
        if self.due_date and self.status != TodoStatus.COMPLETED:
            is_overdue = datetime.now() > self.due_date

        return TodoResponse(
            id=self.id,
            title=self.title,
            description=self.description,
            priority=self.priority,
            status=self.status,
            due_date=self.due_date,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_overdue=is_overdue,
        )
