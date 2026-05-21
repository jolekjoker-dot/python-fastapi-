"""
第4步：Pydantic 数据校验

学习目标：
- 掌握 BaseModel 的使用
- 学会使用 Field 进行字段校验
- 理解嵌套模型
- 了解枚举类型和模型继承

运行方式：
    uvicorn main:app --reload --port 8003
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from enum import Enum

app = FastAPI(title="Pydantic 数据校验")

# ==================== 基础模型 ====================

class Item(BaseModel):
    """
    基础项目模型

    Pydantic 会自动校验数据类型
    """
    name: str                              # 必填，字符串
    description: str | None = None         # 可选，字符串或 None
    price: float                           # 必填，浮点数
    tax: float | None = None               # 可选
    tags: list[str] = []                   # 可选，字符串列表，默认空列表


@app.post("/items/basic/")
async def create_basic_item(item: Item):
    """基础模型示例"""
    return item.model_dump()


# ==================== Field 字段校验 ====================

class Product(BaseModel):
    """
    使用 Field 进行字段校验

    Field 参数说明：
    - ... : 必填字段
    - None : 可选字段，有默认值
    - min_length/max_length : 字符串长度
    - gt/ge/lt/le : 数字范围（大于/大于等于/小于/小于等于）
    - pattern : 正则表达式
    - description : 字段描述（显示在文档中）
    - example : 示例值
    """
    name: str = Field(
        ...,                           # 必填
        min_length=1,                  # 最小长度
        max_length=100,                # 最大长度
        description="产品名称",
        example="Python 书籍",
    )
    price: float = Field(
        ...,                           # 必填
        gt=0,                          # 大于 0
        le=10000,                      # 小于等于 10000
        description="产品价格",
        example=99.9,
    )
    quantity: int = Field(
        default=0,                     # 默认值为 0
        ge=0,                          # 大于等于 0
        le=10000,                      # 小于等于 10000
        description="库存数量",
        example=100,
    )
    description: str | None = Field(
        default=None,
        max_length=500,                # 最大长度 500
        description="产品描述",
    )
    sku: str = Field(
        ...,
        pattern=r"^[A-Z]{3}-\d{4}$",  # 正则表达式：3个大写字母-4个数字
        description="SKU 编号",
        example="ABC-1234",
    )


@app.post("/products/")
async def create_product(product: Product):
    """带校验的产品创建"""
    return {
        "product": product.model_dump(),
        "message": "Product created successfully"
    }


# ==================== 枚举类型 ====================

class Priority(str, Enum):
    """优先级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Status(str, Enum):
    """状态枚举"""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class Task(BaseModel):
    """任务模型，使用枚举限制可选值"""
    title: str
    priority: Priority = Priority.MEDIUM  # 默认值为 MEDIUM
    status: Status = Status.DRAFT          # 默认值为 DRAFT
    assignee: str | None = None


@app.post("/tasks/")
async def create_task(task: Task):
    """
    创建任务

    请求体示例：
    {
        "title": "完成 FastAPI 学习",
        "priority": "high",
        "status": "active",
        "assignee": "张三"
    }
    """
    return task.model_dump()


@app.get("/tasks/priorities/")
async def get_priorities():
    """获取所有可用的优先级"""
    return {
        "priorities": [p.value for p in Priority],
        "descriptions": {
            "low": "低优先级",
            "medium": "中优先级",
            "high": "高优先级",
            "urgent": "紧急",
        }
    }


# ==================== 嵌套模型 ====================

class Address(BaseModel):
    """地址模型"""
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=50)
    state: str = Field(..., min_length=1, max_length=50)
    zip_code: str = Field(..., pattern=r"^\d{6}$")  # 6位数字
    country: str = Field(default="中国", max_length=50)


class ContactInfo(BaseModel):
    """联系信息模型"""
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    phone: str | None = Field(None, pattern=r"^1[3-9]\d{9}$")  # 中国手机号
    website: str | None = None


class Company(BaseModel):
    """公司模型（包含嵌套）"""
    name: str = Field(..., min_length=1, max_length=100)
    address: Address                     # 嵌套地址模型
    contact: ContactInfo                 # 嵌套联系信息模型
    employees: int = Field(default=0, ge=0)
    founded_year: int | None = Field(None, ge=1900, le=2024)


@app.post("/companies/")
async def create_company(company: Company):
    """
    创建公司（嵌套模型）

    请求体示例：
    {
        "name": "Python 科技",
        "address": {
            "street": "科技路 123 号",
            "city": "北京",
            "state": "北京",
            "zip_code": "100000",
            "country": "中国"
        },
        "contact": {
            "email": "info@python-tech.com",
            "phone": "13800138000",
            "website": "https://python-tech.com"
        },
        "employees": 100,
        "founded_year": 2020
    }
    """
    return {
        "company": company.model_dump(),
        "message": f"Company {company.name} created successfully"
    }


# ==================== 模型继承 ====================

class ItemBase(BaseModel):
    """项目基础模型"""
    name: str
    description: str | None = None
    price: float = Field(..., gt=0)


class ItemCreate(ItemBase):
    """创建项目的请求模型"""
    pass


class ItemUpdate(BaseModel):
    """更新项目的请求模型（所有字段可选）"""
    name: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0)


class ItemInDB(ItemBase):
    """数据库中的项目模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True


class ItemResponse(ItemBase):
    """返回给客户端的项目模型"""
    id: int
    is_active: bool


# 模拟数据库
items_db: dict[int, ItemInDB] = {}


@app.post("/items/v2/", response_model=ItemResponse)
async def create_item_v2(item: ItemCreate):
    """创建项目（使用继承的模型）"""
    new_id = max(items_db.keys(), default=0) + 1
    now = datetime.now()

    db_item = ItemInDB(
        id=new_id,
        created_at=now,
        updated_at=now,
        **item.model_dump(),
    )
    items_db[new_id] = db_item

    return ItemResponse(**db_item.model_dump())


@app.patch("/items/v2/{item_id}", response_model=ItemResponse)
async def update_item_v2(item_id: int, item: ItemUpdate):
    """更新项目（部分更新）"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item = items_db[item_id]

    # 只更新提供的字段
    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db_item.updated_at = datetime.now()

    return ItemResponse(**db_item.model_dump())


# ==================== 自定义验证器 ====================

class UserRegistration(BaseModel):
    """用户注册模型，带自定义验证"""
    username: str = Field(..., min_length=3, max_length=20)
    email: str
    password: str = Field(..., min_length=8)
    confirm_password: str
    age: int = Field(..., ge=18, le=120)

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """用户名只能包含字母和数字"""
        if not v.isalnum():
            raise ValueError("用户名只能包含字母和数字")
        return v

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        """邮箱必须包含 @"""
        if "@" not in v:
            raise ValueError("邮箱格式不正确")
        return v.lower()  # 转换为小写

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """确认密码必须与密码一致"""
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("两次密码不一致")
        return v


@app.post("/register/")
async def register_user(user: UserRegistration):
    """
    用户注册（自定义验证）

    请求体示例：
    {
        "username": "zhangsan",
        "email": "zhangsan@example.com",
        "password": "password123",
        "confirm_password": "password123",
        "age": 25
    }
    """
    return {
        "username": user.username,
        "email": user.email,
        "message": "注册成功"
    }


# ==================== 动态模型 ====================

def create_dynamic_model(
    required_fields: list[str],
    optional_fields: list[str] | None = None,
) -> type[BaseModel]:
    """
    动态创建 Pydantic 模型

    这是一个高级用法，展示 Pydantic 的灵活性
    """
    fields = {}
    for field_name in required_fields:
        fields[field_name] = (str, ...)
    for field_name in (optional_fields or []):
        fields[field_name] = (str | None, None)

    return BaseModel.__class__(
        "DynamicModel",
        (BaseModel,),
        {"__annotations__": {k: v[0] for k, v in fields.items()}},
    )


# ==================== 练习用的接口 ====================

@app.get("/examples/")
async def get_examples():
    """获取各种模型的示例数据"""
    return {
        "item_example": {
            "name": "Python 书籍",
            "description": "学习 Python 的好书",
            "price": 59.9,
            "tax": 5.0,
            "tags": ["python", "programming"],
        },
        "product_example": {
            "name": "FastAPI 教程",
            "price": 39.9,
            "quantity": 100,
            "description": "FastAPI 入门到精通",
            "sku": "FAI-1234",
        },
        "task_example": {
            "title": "完成项目",
            "priority": "high",
            "status": "active",
            "assignee": "张三",
        },
    }
