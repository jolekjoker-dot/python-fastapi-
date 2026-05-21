# FastAPI 日程记录项目 - 详细执行与学习指南

> 本指南专为零基础新手设计，逐步带你从 Python 基础到完成第一个 FastAPI 项目。

---

## 项目总览

```
fastapi/
├── learning_guide.md          # 本学习文档
├── requirements.txt           # Python 依赖列表
├── phase1_basics/             # 第一阶段：Python 基础练习
│   ├── 01_variables.py        # 变量和数据类型
│   ├── 02_control_flow.py     # 条件判断和循环
│   ├── 03_functions.py        # 函数定义和使用
│   ├── 04_classes.py          # 类和面向对象
│   ├── 05_collections.py      # 列表、字典、集合
│   ├── 06_error_handling.py   # 异常处理
│   ├── 07_type_hints.py       # 类型提示
│   ├── 08_async_basics.py     # 异步基础
│   └── practice_exercises.py  # 阶段练习题
├── phase2_fastapi/            # 第二阶段：FastAPI 核心
│   ├── step1_hello/           # 第1步：Hello World
│   │   └── main.py
│   ├── step2_routing/         # 第2步：路由与请求处理
│   │   └── main.py
│   ├── step3_response/        # 第3步：响应处理
│   │   └── main.py
│   ├── step4_pydantic/        # 第4步：Pydantic 数据校验
│   │   └── main.py
│   └── todo_project/          # 阶段实战：待办事项 API
│       ├── main.py            # 主应用入口
│       ├── models.py          # 数据模型
│       ├── schemas.py         # Pydantic 模式
│       └── memory_store.py    # 内存数据存储
└── README.md                  # 项目说明
```

---

# 第一阶段：前置知识准备（1-3 天）

## 学习目标
- 掌握 Python 3.9+ 基础语法
- 理解类型提示和异步概念
- 会使用虚拟环境和包管理

---

## 1.1 环境准备

### 安装 Python

1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.11 或更高版本
3. 安装时 **务必勾选** "Add Python to PATH"
4. 验证安装：
   ```bash
   python --version
   # 输出类似：Python 3.11.x
   ```

### 安装代码编辑器

推荐使用 VS Code（你已经在用了）+ Python 扩展：
1. 在 VS Code 中按 `Ctrl+Shift+X`
2. 搜索 "Python"，安装 Microsoft 官方扩展

---

## 1.2 Python 基础语法学习路径

### 学习顺序和对应文件

| 序号 | 主题 | 文件 | 预计时间 | 核心知识点 |
|------|------|------|----------|------------|
| 1 | 变量和数据类型 | `01_variables.py` | 30分钟 | int, str, float, bool, 类型转换 |
| 2 | 条件和循环 | `02_control_flow.py` | 45分钟 | if/elif/else, for, while, break |
| 3 | 函数 | `03_functions.py` | 45分钟 | def, 参数, 返回值, 默认参数 |
| 4 | 类和对象 | `04_classes.py` | 1小时 | class, __init__, 方法, 继承 |
| 5 | 集合类型 | `05_collections.py` | 45分钟 | list, dict, set, 列表推导式 |
| 6 | 异常处理 | `06_error_handling.py` | 30分钟 | try/except/finally, 自定义异常 |
| 7 | 类型提示 | `07_type_hints.py` | 30分钟 | int, str, Optional, List, Dict |
| 8 | 异步基础 | `08_async_basics.py` | 30分钟 | async/await, asyncio 基础 |

### 如何运行练习文件

```bash
# 进入项目目录
cd phase1_basics

# 运行单个文件
python 01_variables.py

# 或者使用 Python 交互模式测试代码片段
python -i 01_variables.py
```

---

## 1.3 第一阶段学习要点速查

### 变量和数据类型
```python
# Python 是动态类型语言，不需要声明类型
name = "张三"           # 字符串 str
age = 25               # 整数 int
height = 175.5         # 浮点数 float
is_student = True      # 布尔值 bool

# 类型转换
age_str = str(age)     # "25"
age_int = int("25")    # 25
```

### 函数定义
```python
def greet(name: str, greeting: str = "你好") -> str:
    """返回问候语"""
    return f"{greeting}, {name}!"

# 调用
message = greet("张三")           # "你好, 张三!"
message = greet("张三", "早上好")  # "早上好, 张三!"
```

### 类定义
```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def introduce(self) -> str:
        return f"我叫{self.name}，今年{self.age}岁"

# 使用
person = Person("张三", 25)
print(person.introduce())
```

### 列表和字典
```python
# 列表 - 有序集合
todos = ["学习 Python", "写代码", "测试"]
todos.append("部署")        # 添加元素
first = todos[0]           # 访问元素

# 字典 - 键值对
person = {
    "name": "张三",
    "age": 25,
    "skills": ["Python", "FastAPI"]
}
name = person["name"]      # 访问值
person["email"] = "..."    # 添加键值对
```

### 异常处理
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零")
except Exception as e:
    print(f"发生错误: {e}")
finally:
    print("总是执行")
```

---

## 1.4 第一阶段检验标准

完成以下任务，说明你已准备好进入第二阶段：

- [ ] 能独立写一个函数，接收参数并返回结果
- [ ] 能定义一个类，包含属性和方法
- [ ] 能使用列表存储多个数据，并遍历处理
- [ ] 能使用字典存储键值对数据
- [ ] 能使用 try-except 处理可能的错误
- [ ] 理解类型提示的作用（虽然不强制）

---

# 第二阶段：FastAPI 核心入门（1-2 周）

## 学习目标
- 掌握 FastAPI 的核心语法
- 能独立编写 CRUD 接口
- 理解并使用 Pydantic 进行数据校验
- 能阅读自动生成的 API 文档

---

## 2.1 第1步：环境搭建与 Hello World（第1天）

### 学习内容
- 创建虚拟环境
- 安装 FastAPI 和 Uvicorn
- 编写第一个接口
- 理解 ASGI 服务器概念

### 执行步骤

#### 步骤1：创建虚拟环境
```bash
# 在项目根目录执行
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 激活后，命令行前面会出现 (venv) 标识
```

**为什么要用虚拟环境？**
- 隔离项目依赖，避免不同项目之间的包版本冲突
- 方便导出和复现依赖列表
- 是 Python 开发的最佳实践

#### 步骤2：安装依赖
```bash
pip install fastapi uvicorn[standard]
```

**这两个包是什么？**
- `fastapi`: Web 框架，帮你快速写 API
- `uvicorn`: ASGI 服务器，负责运行你的代码，处理 HTTP 请求

#### 步骤3：编写第一个接口

在 `phase2_fastapi/step1_hello/main.py` 中编写代码。

#### 步骤4：启动服务
```bash
cd phase2_fastapi/step1_hello
uvicorn main:app --reload --port 8000
```

**命令解释：**
- `uvicorn`: 启动 ASGI 服务器
- `main:app`: 找到 main.py 文件中的 app 对象
- `--reload`: 代码修改后自动重启（开发模式）
- `--port 8000`: 使用 8000 端口

#### 步骤5：访问文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 关键概念

| 概念 | 说明 |
|------|------|
| ASGI | 异步服务器网口接口，比 WSGI 更现代，支持异步 |
| Uvicorn | 高性能 ASGI 服务器 |
| Swagger UI | 自动生成的 API 文档，可以在线测试接口 |
| 路由 (Route) | URL 路径和处理函数的映射关系 |
| 装饰器 | `@app.get("/")` 这种语法，用于定义路由 |

---

## 2.2 第2步：路由与请求处理（第2-3天）

### 学习内容
- 路径参数（Path Parameters）
- 查询参数（Query Parameters）
- 请求体（Request Body）
- 混合使用多种参数

### 关键概念详解

#### 路径参数
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

**特点：**
- 路径中的 `{item_id}` 是占位符
- 函数参数名必须和路径中的名称一致
- FastAPI 会自动进行类型转换和校验
- 访问 `/items/123` → item_id = 123
- 访问/items/abc` → 返回 422 错误（类型不匹配）

#### 查询参数
```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

**特点：**
- 不在路径中的函数参数，自动成为查询参数
- 可以设置默认值，变成可选参数
- 访问 `/items/?skip=20&limit=5`

#### 请求体
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
async def create_item(item: Item):
    return item
```

**特点：**
- 使用 Pydantic 模型定义请求数据结构
- FastAPI 自动解析 JSON 请求体
- 自动进行数据校验和类型转换
- 自动生成文档中的请求体示例

---

## 2.3 第3步：响应处理（第4-5天）

### 学习内容
- 响应模型（response_model）
- 状态码（status_code）
- 错误响应（HTTPException）
- 响应头设置

### 关键概念

#### 响应模型
```python
class ItemResponse(BaseModel):
    id: int
    name: str
    # 注意：没有 price 字段，会被过滤掉

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    return {"id": 1, "name": item.name, "price": item.price}
    # 即使返回了 price，响应中也不会包含
```

**作用：**
- 过滤返回数据，隐藏敏感字段
- 自动进行响应数据校验
- 在文档中显示响应数据结构

#### 状态码
```python
@app.post("/items/", status_code=201)
async def create_item(item: Item):
    return item
```

**常用状态码：**
- 200: 成功（默认）
- 201: 创建成功
- 204: 成功但无内容
- 400: 请求错误
- 401: 未认证
- 403: 无权限
- 404: 资源不存在
- 422: 数据校验失败
- 500: 服务器错误

#### 错误响应
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found"
        )
    return items[item_id]
```

---

## 2.4 第4步：Pydantic 数据校验（第6-7天）

### 学习内容
- BaseModel 基础用法
- Field 字段校验
- 嵌套模型
- 枚举类型
- 模型继承

### 关键概念

#### 字段校验
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, le=10000)
    description: str | None = Field(None, max_length=500)
```

**Field 参数说明：**
- `...`: 必填字段
- `min_length`, `max_length`: 字符串长度限制
- `gt`, `ge`, `lt`, `le`: 数字范围（大于、大于等于、小于、小于等于）
- `None`: 可选字段，有默认值

#### 嵌套模型
```python
class Address(BaseModel):
    city: str
    street: str

class User(BaseModel):
    name: str
    address: Address  # 嵌套其他模型
```

#### 枚举类型
```python
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Todo(BaseModel):
    title: str
    priority: Priority = Priority.MEDIUM
```

---

## 2.5 阶段实战：待办事项 API（第8-10天）

### 项目结构
```
todo_project/
├── main.py            # 主应用，路由定义
├── models.py          # Pydantic 模型定义
├── schemas.py         # 请求/响应模式
└── memory_store.py    # 内存数据存储（模拟数据库）
```

### 实现的功能
1. GET /todos - 获取所有待办
2. GET /todos/{todo_id} - 获取单个待办
3. POST /todos - 创建新待办
4. PUT /todos/{todo_id} - 更新待办
5. DELETE /todos/{todo_id} - 删除待办

### 学习收获
- 理解项目结构组织
- 掌握完整的 CRUD 操作
- 学会分离数据模型和业务逻辑
- 体验 FastAPI 的开发效率

---

## 2.6 第二阶段检验标准

完成以下任务，说明你已掌握 FastAPI 核心：

- [ ] 能独立启动 FastAPI 服务并访问文档
- [ ] 能定义路径参数、查询参数和请求体
- [ ] 能使用 Pydantic 模型进行数据校验
- [ ] 能返回正确的状态码和错误信息
- [ ] 能实现完整的 CRUD 接口
- [ ] 能在 Swagger UI 中测试所有接口

---

# 学习建议

## 每日学习计划

### 第一阶段（3天）
- Day 1: 变量、数据类型、条件、循环（01-02）
- Day 2: 函数、类和对象（03-04）
- Day 3: 集合类型、异常处理、类型提示（05-07）+ 练习

### 第二阶段（10天）
- Day 1-2: 环境搭建 + Hello World（step1）
- Day 3-4: 路由和请求处理（step2）
- Day 5-6: 响应处理（step3）
- Day 7-8: Pydantic 数据校验（step4）
- Day 9-10: 待办事项实战项目

## 遇到问题怎么办？

1. **仔细阅读错误信息** - Python 的错误提示通常很详细
2. **查看自动生成的文档** - Swagger UI 是最好的调试工具
3. **使用 print 调试** - 在关键位置打印变量值
4. **逐行执行** - 不理解时，把代码拆开一步步运行
5. **搜索错误信息** - 把错误信息复制到搜索引擎

## 推荐学习资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/) - 最权威的教程
- [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/) - Python 基础
- [Pydantic 官方文档](https://docs.pydantic.dev/) - 数据校验库

---

# 下一步预告

完成前两阶段后，第三阶段将学习：
- 数据库集成（SQLite + SQLAlchemy）
- 用户认证（JWT）
- 项目部署

继续加油！
