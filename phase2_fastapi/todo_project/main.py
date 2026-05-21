"""
待办事项 API - 阶段实战项目

功能：
- 获取所有待办事项
- 获取单个待办事项详情
- 创建新待办事项
- 更新待办事项
- 删除待办事项
- 标记完成
- 获取统计信息

运行方式：
    uvicorn main:app --reload --port 8000

访问文档：
    http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, Query
from datetime import datetime

from models import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoListResponse,
    TodoStatus,
    Priority,
)
from memory_store import todo_store

# 创建 FastAPI 应用
app = FastAPI(
    title="待办事项 API",
    description="一个简单的待办事项管理 API，用于学习 FastAPI",
    version="0.1.0",
)


# ==================== 根路由 ====================

@app.get("/")
async def root():
    """根路由 - 返回欢迎信息"""
    return {
        "message": "欢迎使用待办事项 API",
        "docs": "/docs",
        "version": "0.1.0",
    }


# ==================== 获取所有待办事项 ====================

@app.get("/todos", response_model=TodoListResponse)
async def get_todos(
    status: TodoStatus | None = Query(None, description="按状态过滤"),
    priority: Priority | None = Query(None, description="按优先级过滤"),
):
    """
    获取所有待办事项

    可选参数：
    - status: 按状态过滤（pending/in_progress/completed）
    - priority: 按优先级过滤（low/medium/high）
    """
    todos = todo_store.get_all(status=status, priority=priority)
    stats = todo_store.get_stats()

    return TodoListResponse(
        todos=[todo.to_response() for todo in todos],
        **stats,
    )


# ==================== 获取单个待办事项 ====================

@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int):
    """
    获取单个待办事项详情

    - todo_id: 待办事项 ID
    """
    todo = todo_store.get_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=404,
            detail=f"待办事项 {todo_id} 不存在",
        )
    return todo.to_response()


# ==================== 创建待办事项 ====================

@app.post("/todos", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate):
    """
    创建新待办事项

    请求体示例：
    {
        "title": "学习 FastAPI",
        "description": "完成 FastAPI 教程",
        "priority": "high",
        "due_date": "2024-12-31T00:00:00"
    }
    """
    created_todo = todo_store.create(todo)
    return created_todo.to_response()


# ==================== 更新待办事项 ====================

@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """
    更新待办事项

    所有字段都是可选的，只更新提供的字段

    请求体示例：
    {
        "title": "新标题",
        "status": "in_progress"
    }
    """
    # 检查待办事项是否存在
    existing_todo = todo_store.get_by_id(todo_id)
    if not existing_todo:
        raise HTTPException(
            status_code=404,
            detail=f"待办事项 {todo_id} 不存在",
        )

    # 更新
    updated_todo = todo_store.update(todo_id, todo_update)
    return updated_todo.to_response()


# ==================== 删除待办事项 ====================

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    """
    删除待办事项

    使用软删除（标记为已删除，不实际删除数据）
    """
    success = todo_store.delete(todo_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"待办事项 {todo_id} 不存在",
        )
    return None


# ==================== 标记完成 ====================

@app.patch("/todos/{todo_id}/complete", response_model=TodoResponse)
async def complete_todo(todo_id: int):
    """
    标记待办事项为完成

    这是一个快捷操作，等同于 PUT /todos/{todo_id} {"status": "completed"}
    """
    todo = todo_store.complete(todo_id)
    if not todo:
        raise HTTPException(
            status_code=404,
            detail=f"待办事项 {todo_id} 不存在",
        )
    return todo.to_response()


# ==================== 获取统计信息 ====================

@app.get("/todos/stats/summary")
async def get_stats():
    """
    获取待办事项统计信息

    返回：
    - total: 总数
    - pending: 待处理数
    - in_progress: 进行中数
    - completed: 已完成数
    """
    return todo_store.get_stats()


# ==================== 批量操作 ====================

@app.post("/todos/batch", response_model=list[TodoResponse], status_code=201)
async def create_todos_batch(todos: list[TodoCreate]):
    """
    批量创建待办事项

    请求体示例：
    [
        {"title": "任务1", "priority": "high"},
        {"title": "任务2", "priority": "low"}
    ]
    """
    created_todos = []
    for todo in todos:
        created = todo_store.create(todo)
        created_todos.append(created.to_response())
    return created_todos


# ==================== 搜索 ====================

@app.get("/todos/search/{keyword}", response_model=list[TodoResponse])
async def search_todos(keyword: str):
    """
    搜索待办事项

    在标题和描述中搜索关键词
    """
    all_todos = todo_store.get_all()
    results = [
        todo.to_response()
        for todo in all_todos
        if keyword.lower() in todo.title.lower()
        or (todo.description and keyword.lower() in todo.description.lower())
    ]
    return results


# ==================== 启动说明 ====================
# 运行命令：
# uvicorn main:app --reload --port 8000
#
# API 端点：
# GET    /todos              - 获取所有待办
# GET    /todos/{id}         - 获取单个待办
# POST   /todos              - 创建待办
# PUT    /todos/{id}         - 更新待办
# DELETE /todos/{id}         - 删除待办
# PATCH  /todos/{id}/complete - 标记完成
# GET    /todos/stats/summary - 统计信息
# POST   /todos/batch        - 批量创建
# GET    /todos/search/{keyword} - 搜索
