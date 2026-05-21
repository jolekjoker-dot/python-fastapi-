# FastAPI 日程记录项目

一个用于学习 FastAPI 的简单日程记录项目，专为新手设计。

## 项目结构

```
fastapi/
├── learning_guide.md          # 详细学习指南
├── requirements.txt           # Python 依赖
├── README.md                  # 项目说明
├── phase1_basics/             # 第一阶段：Python 基础
│   ├── 01_variables.py        # 变量和数据类型
│   ├── 02_control_flow.py     # 条件和循环
│   ├── 03_functions.py        # 函数
│   ├── 04_classes.py          # 类和对象
│   ├── 05_collections.py      # 列表、字典、集合
│   ├── 06_error_handling.py   # 异常处理
│   ├── 07_type_hints.py       # 类型提示
│   ├── 08_async_basics.py     # 异步基础
│   └── practice_exercises.py  # 练习题
└── phase2_fastapi/            # 第二阶段：FastAPI 核心
    ├── step1_hello/           # Hello World
    ├── step2_routing/         # 路由与请求处理
    ├── step3_response/        # 响应处理
    ├── step4_pydantic/        # Pydantic 数据校验
    └── todo_project/          # 待办事项实战
```

## 快速开始

### 1. 安装 Python

访问 https://www.python.org/downloads/ 下载 Python 3.11+

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行项目

```bash
# 进入项目目录
cd phase2_fastapi/todo_project

# 启动服务
uvicorn main:app --reload --port 8000
```

### 5. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 学习路径

### 第一阶段：Python 基础（1-3 天）

按照 `phase1_basics/` 目录中的文件顺序学习：

1. 变量和数据类型
2. 条件判断和循环
3. 函数定义和使用
4. 类和面向对象
5. 列表、字典、集合
6. 异常处理
7. 类型提示
8. 异步基础

### 第二阶段：FastAPI 核心（1-2 周）

按照 `phase2_fastapi/` 目录中的步骤学习：

1. **Hello World** - 环境搭建和第一个接口
2. **路由处理** - 路径参数、查询参数、请求体
3. **响应处理** - 状态码、错误处理、响应模型
4. **Pydantic** - 数据校验、模型继承、枚举
5. **实战项目** - 待办事项 CRUD API

## API 端点

待办事项 API 提供以下端点：

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /todos | 获取所有待办 |
| GET | /todos/{id} | 获取单个待办 |
| POST | /todos | 创建待办 |
| PUT | /todos/{id} | 更新待办 |
| DELETE | /todos/{id} | 删除待办 |
| PATCH | /todos/{id}/complete | 标记完成 |
| GET | /todos/stats/summary | 获取统计 |
| POST | /todos/batch | 批量创建 |
| GET | /todos/search/{keyword} | 搜索 |

## 下一步

完成前两阶段后，可以继续学习：

- 第三阶段：数据库集成（SQLite + SQLAlchemy）
- 第四阶段：用户认证（JWT）
- 第五阶段：项目部署

## 参考资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/)
- [Pydantic 官方文档](https://docs.pydantic.dev/)
