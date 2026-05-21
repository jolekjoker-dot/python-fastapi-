"""
第3步：响应处理

学习目标：
- 掌握响应模型（response_model）
- 学会设置状态码
- 理解错误响应（HTTPException）
- 了解响应头设置

运行方式：
    uvicorn main:app --reload --port 8002
"""

from fastapi import FastAPI, HTTPException, Response, Header
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI(title="响应处理")

# ==================== 数据存储（模拟数据库）====================

fake_items_db = {
    1: {"id": 1, "name": "Python 书籍", "price": 59.9, "secret_key": "hidden123"},
    2: {"id": 2, "name": "FastAPI 教程", "price": 39.9, "secret_key": "hidden456"},
    3: {"id": 3, "name": "编程笔记本", "price": 25.0, "secret_key": "hidden789"},
}

# ==================== 响应模型 ====================
# response_model 用于过滤返回数据，隐藏敏感字段

class ItemPublic(BaseModel):
    """公开的项目信息（不包含敏感字段）"""
    id: int
    name: str
    price: float

class ItemInternal(BaseModel):
    """内部的项目信息（包含所有字段）"""
    id: int
    name: str
    price: float
    secret_key: str


@app.get("/items/{item_id}", response_model=ItemPublic)
async def read_item(item_id: int):
    """
    使用 response_model 过滤响应

    即使函数返回了 secret_key，响应中也不会包含
    因为 ItemPublic 模型中没有定义这个字段
    """
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]


@app.get("/items/", response_model=list[ItemPublic])
async def read_items():
    """返回列表，每个元素都经过 response_model 过滤"""
    return list(fake_items_db.values())


# ==================== 状态码 ====================

class ItemCreate(BaseModel):
    """创建项目的请求模型"""
    name: str
    price: float

class ItemResponse(BaseModel):
    """创建成功的响应模型"""
    id: int
    name: str
    price: float
    created_at: datetime
    message: str = "Item created successfully"


@app.post("/items/", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    """
    创建项目，返回 201 状态码

    201 Created - 表示资源创建成功
    """
    new_id = max(fake_items_db.keys()) + 1
    new_item = {
        "id": new_id,
        "name": item.name,
        "price": item.price,
        "secret_key": f"secret_{new_id}",
        "created_at": datetime.now(),
    }
    fake_items_db[new_id] = new_item
    return new_item


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """
    删除项目，返回 204 状态码

    204 No Content - 表示成功但没有返回内容
    """
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_items_db[item_id]
    return None  # 204 状态码不返回内容


# ==================== 错误响应 ====================

class ErrorResponse(BaseModel):
    """错误响应模型"""
    detail: str
    error_code: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now)


@app.get("/items/{item_id}/details", response_model=ItemPublic)
async def item_details(item_id: int):
    """
    带详细错误信息的接口

    使用 HTTPException 抛出错误
    """
    # 404 - 资源不存在
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=404,
            detail=f"项目 {item_id} 不存在",
            headers={"X-Error-Code": "ITEM_NOT_FOUND"},
        )

    # 模拟其他错误
    if item_id == 999:
        raise HTTPException(
            status_code=500,
            detail="服务器内部错误",
        )

    return fake_items_db[item_id]


# 多个错误状态码
@app.put("/items/{item_id}", response_model=ItemPublic)
async def update_item(item_id: int, item: ItemCreate):
    """
    更新项目

    可能的错误：
    - 404: 项目不存在
    - 422: 数据校验失败（自动处理）
    """
    # 404
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=404,
            detail=f"项目 {item_id} 不存在",
        )

    # 模拟业务规则校验
    if item.price < 0:
        raise HTTPException(
            status_code=400,
            detail="价格不能为负数",
        )

    # 更新数据
    fake_items_db[item_id].update({
        "name": item.name,
        "price": item.price,
    })
    return fake_items_db[item_id]


# ==================== 自定义响应 ====================

@app.get("/items/{item_id}/custom-header")
async def item_with_custom_header(item_id: int):
    """
    自定义响应头

    可以设置自定义的响应头
    """
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    return Response(
        content=f"Item {item_id} data",
        media_type="text/plain",
        headers={
            "X-Item-ID": str(item_id),
            "X-Custom-Header": "custom-value",
        },
    )


@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    文件下载响应

    设置 Content-Disposition 响应头
    """
    content = f"File content of {filename}"
    return Response(
        content=content,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )


# ==================== 响应头读取 ====================

@app.get("/check-header/")
async def check_header(
    x_token: str | None = Header(None),  # 从请求头读取
):
    """
    读取请求头

    可以使用 Header() 读取请求头
    """
    if x_token is None:
        raise HTTPException(
            status_code=401,
            detail="X-Token header missing",
        )

    return {
        "x_token": x_token,
        "message": "Token is valid",
    }


# ==================== 不同响应格式 ====================

@app.get("/html/")
async def html_response():
    """返回 HTML 响应"""
    html_content = """
    <html>
        <head><title>FastAPI HTML</title></head>
        <body>
            <h1>Hello from FastAPI!</h1>
            <p>This is an HTML response.</p>
        </body>
    </html>
    """
    return Response(content=html_content, media_type="text/html")


@app.get("/plain-text/")
async def plain_text_response():
    """返回纯文本响应"""
    return Response(content="Hello, World!", media_type="text/plain")


# ==================== 统一响应格式 ====================

class ApiResponse(BaseModel):
    """统一 API 响应格式"""
    success: bool
    data: dict | list | None = None
    message: str = ""
    error: str | None = None


@app.get("/unified/items/{item_id}", response_model=ApiResponse)
async def unified_read_item(item_id: int):
    """
    统一响应格式示例

    所有接口返回相同的数据结构
    """
    if item_id not in fake_items_db:
        return ApiResponse(
            success=False,
            error=f"Item {item_id} not found",
        )

    return ApiResponse(
        success=True,
        data=fake_items_db[item_id],
        message="Item retrieved successfully",
    )


@app.post("/unified/items/", response_model=ApiResponse)
async def unified_create_item(item: ItemCreate):
    """统一响应格式 - 创建"""
    new_id = max(fake_items_db.keys()) + 1
    new_item = {
        "id": new_id,
        "name": item.name,
        "price": item.price,
        "secret_key": f"secret_{new_id}",
    }
    fake_items_db[new_id] = new_item

    return ApiResponse(
        success=True,
        data=ItemPublic(**new_item).model_dump(),
        message="Item created successfully",
    )
