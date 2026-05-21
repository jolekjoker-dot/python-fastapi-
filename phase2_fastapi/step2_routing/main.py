"""
第2步：路由与请求处理

学习目标：
- 掌握路径参数（Path Parameters）
- 掌握查询参数（Query Parameters）
- 掌握请求体（Request Body）
- 学会混合使用多种参数

运行方式：
    uvicorn main:app --reload --port 8001
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="路由与请求处理")

# ==================== 路径参数 ====================
# 路径参数是 URL 的一部分，用 {} 表示

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    路径参数示例

    访问：/items/123
    item_id 会被自动转换为整数

    如果访问 /items/abc，会返回 422 错误（类型不匹配）
    """
    return {"item_id": item_id, "type": type(item_id).__name__}


@app.get("/users/{user_id}/posts/{post_id}")
async def read_user_post(user_id: int, post_id: int):
    """
    多个路径参数

    访问：/users/1/posts/100
    """
    return {
        "user_id": user_id,
        "post_id": post_id,
    }


# 路径参数使用枚举限制值
from enum import Enum

class ModelName(str, Enum):
    ALEXNET = "alexnet"
    RESNET = "resnet"
    LENET = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """
    枚举路径参数

    只接受预定义的值：alexnet, resnet, lenet
    """
    return {
        "model_name": model_name,
        "message": f"Deep Learning FTW with {model_name.value}!"
    }


# ==================== 查询参数 ====================
# 查询参数是 URL ? 后面的键值对

@app.get("/items/")
async def read_items(
    skip: int = 0,       # 默认值为 0，可选参数
    limit: int = 10,     # 默认值为 10，可选参数
):
    """
    查询参数示例

    访问方式：
    - /items/ - 使用默认值
    - /items/?skip=20 - 自定义 skip
    - /items/?skip=20&limit=5 - 自定义两个参数
    """
    return {
        "skip": skip,
        "limit": limit,
        "message": f"返回第 {skip} 到 {skip + limit} 条数据"
    }


@app.get("/search/")
async def search(
    q: str,                    # 必填参数（没有默认值）
    category: str = "all",     # 可选参数
    min_price: float = 0.0,    # 可选参数
    max_price: float = 1000.0, # 可选参数
):
    """
    搜索接口

    访问方式：
    - /search?q=python - 只传必填参数
    - /search?q=python&category=books&max_price=50 - 传多个参数
    """
    return {
        "query": q,
        "category": category,
        "price_range": f"{min_price} - {max_price}",
    }


# 可选参数（使用 None 作为默认值）
@app.get("/items/{item_id}/details")
async def item_details(
    item_id: int,
    short: bool = False,  # 布尔类型查询参数
):
    """
    可选参数示例

    访问方式：
    - /items/1/details - short=False
    - /items/1/details?short=true - short=True
    - /items/1/details?short=1 - short=True（1/yes/on/true 都是 True）
    """
    details = {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "description": f"This is a detailed description of item {item_id}",
        "price": 99.99,
    }

    if short:
        return {"item_id": item_id, "name": details["name"]}

    return details


# ==================== 请求体 ====================
# 请求体用于发送复杂数据（通常是 JSON）

# 定义 Pydantic 模型
class Item(BaseModel):
    """项目模型"""
    name: str                    # 必填字段
    description: str | None = None  # 可选字段
    price: float                 # 必填字段
    tax: float | None = None     # 可选字段


@app.post("/items/")
async def create_item(item: Item):
    """
    创建项目（带请求体）

    发送 POST 请求到 /items/
    请求体示例：
    {
        "name": "Foo",
        "description": "A very nice item",
        "price": 35.4,
        "tax": 3.2
    }
    """
    # item 是一个 Pydantic 模型对象
    item_dict = item.model_dump()  # 转换为字典

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict


# ==================== 混合参数 ====================
# 同时使用路径参数、查询参数和请求体

class UserCreate(BaseModel):
    """用户创建模型"""
    username: str
    email: str
    full_name: str | None = None


@app.post("/users/{user_id}/items/")
async def create_user_item(
    user_id: int,           # 路径参数
    item: Item,             # 请求体
    q: str | None = None,   # 查询参数（可选）
):
    """
    混合参数示例

    发送 POST 请求到 /users/1/items/?q=search
    路径中的 1 是 user_id
    ?q=search 是查询参数
    请求体是 Item 对象
    """
    result = {
        "user_id": user_id,
        "item": item.model_dump(),
    }
    if q:
        result.update({"query": q})
    return result


# ==================== 请求体 + 路径参数 ====================

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    更新项目

    路径参数 item_id + 请求体 Item
    """
    return {
        "item_id": item_id,
        "updated_item": item.model_dump(),
        "message": f"Item {item_id} updated successfully"
    }


# ==================== 嵌套模型 ====================

class Address(BaseModel):
    """地址模型"""
    street: str
    city: str
    state: str
    zip_code: str


class Customer(BaseModel):
    """客户模型（包含嵌套的地址）"""
    name: str
    email: str
    address: Address  # 嵌套模型


@app.post("/customers/")
async def create_customer(customer: Customer):
    """
    创建客户（嵌套模型）

    请求体示例：
    {
        "name": "张三",
        "email": "zhangsan@example.com",
        "address": {
            "street": "人民路 123 号",
            "city": "上海",
            "state": "上海",
            "zip_code": "200000"
        }
    }
    """
    return {
        "customer": customer.model_dump(),
        "message": f"Customer {customer.name} created"
    }


# ==================== 列表请求体 ====================

@app.post("/items/batch/")
async def create_items(items: list[Item]):
    """
    批量创建项目

    请求体示例：
    [
        {"name": "Item 1", "price": 10.0},
        {"name": "Item 2", "price": 20.0}
    ]
    """
    return {
        "count": len(items),
        "items": [item.model_dump() for item in items],
        "message": f"Created {len(items)} items"
    }
