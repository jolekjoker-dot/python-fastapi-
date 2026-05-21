"""
第1步：Hello World - FastAPI 入门

学习目标：
- 创建第一个 FastAPI 应用
- 理解路由装饰器
- 启动 Uvicorn 服务器
- 访问自动生成的文档

运行方式：
    uvicorn main:app --reload --port 8000

访问地址：
    - 应用: http://localhost:8000
    - Swagger UI 文档: http://localhost:8000/docs
    - ReDoc 文档: http://localhost:8000/redoc
    - OpenAPI JSON: http://localhost:8000/openapi.json
"""

from fastapi import FastAPI

# 创建 FastAPI 应用实例
# 这是整个应用的核心对象
app = FastAPI(
    title="我的第一个 FastAPI 应用",
    description="这是一个学习 FastAPI 的示例项目",
    version="0.1.0",
)


# ==================== 基础路由 ====================

# @app.get("/") 是一个装饰器
# 它告诉 FastAPI：当收到 GET 请求到 "/" 时，执行下面的函数
@app.get("/")
async def root():
    """
    根路由 - 返回欢迎信息

    这个函数是异步的（使用 async def）
    FastAPI 会自动处理异步调用
    """
    return {"message": "Hello, World!"}


# ==================== 带参数的路由 ====================

@app.get("/hello/{name}")
async def hello_name(name: str):
    """
    带路径参数的路由

    {name} 是路径参数，会被传递给函数
    FastAPI 会自动进行类型转换和校验
    """
    return {"message": f"Hello, {name}!"}


# ==================== 查询参数 ====================

@app.get("/greet")
async def greet(
    name: str = "World",  # 默认值为 "World"
    times: int = 1,       # 默认值为 1
):
    """
    带查询参数的路由

    访问方式：
    - /greet?name=张三&times=3
    - /greet?name=张三
    - /greet（使用默认值）
    """
    messages = [f"Hello, {name}!" for _ in range(times)]
    return {"messages": messages}


# ==================== 返回不同数据类型 ====================

@app.get("/info")
async def info():
    """返回应用信息"""
    return {
        "app_name": "FastAPI 学习项目",
        "version": "0.1.0",
        "docs_url": "/docs",
        "features": [
            "自动生成 API 文档",
            "数据校验",
            "异步支持",
        ]
    }


# ==================== 多个 HTTP 方法 ====================

@app.get("/items")
async def list_items():
    """获取所有项目（GET 请求）"""
    return {"items": ["item1", "item2", "item3"]}


@app.post("/items")
async def create_item():
    """创建新项目（POST 请求）"""
    return {"message": "Item created", "status": "success"}


@app.put("/items/{item_id}")
async def update_item(item_id: int):
    """更新项目（PUT 请求）"""
    return {"message": f"Item {item_id} updated", "status": "success"}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """删除项目（DELETE 请求）"""
    return {"message": f"Item {item_id} deleted", "status": "success"}


# ==================== 启动说明 ====================
# 在终端中运行以下命令启动服务：
#
# uvicorn main:app --reload --port 8000
#
# 参数说明：
# - main: 指 main.py 文件
# - app: 指文件中的 app 变量
# - --reload: 代码修改后自动重启（开发模式）
# - --port 8000: 使用 8000 端口
#
# 启动后访问：
# - http://localhost:8000 - 首页
# - http://localhost:8000/docs - Swagger UI 文档（推荐）
# - http://localhost:8000/redoc - ReDoc 文档
