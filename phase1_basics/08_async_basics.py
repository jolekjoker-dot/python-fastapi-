"""
第8课：异步编程基础

学习目标：
- 理解同步和异步的区别
- 掌握 async/await 语法
- 了解 asyncio 基础用法
- 理解为什么 FastAPI 使用异步
"""

# ==================== 同步 vs 异步 ====================

# 同步：代码按顺序执行，必须等上一个任务完成
# 异步：可以在等待时执行其他任务

import asyncio
import time

# ==================== 同步示例 ====================

def sync_task(name: str, duration: int):
    """同步任务"""
    print(f"开始任务: {name}")
    time.sleep(duration)  # 模拟耗时操作
    print(f"完成任务: {name}")
    return f"{name}的结果"

def run_sync_tasks():
    """运行同步任务"""
    start = time.time()

    result1 = sync_task("任务1", 2)
    result2 = sync_task("任务2", 2)
    result3 = sync_task("任务3", 2)

    end = time.time()
    print(f"同步总耗时: {end - start:.2f}秒")  # 约6秒
    return [result1, result2, result3]

# ==================== 异步示例 ====================

async def async_task(name: str, duration: int):
    """异步任务"""
    print(f"开始任务: {name}")
    await asyncio.sleep(duration)  # 异步等待，不阻塞其他任务
    print(f"完成任务: {name}")
    return f"{name}的结果"

async def run_async_tasks():
    """运行异步任务"""
    start = time.time()

    # asyncio.gather() 并发运行多个任务
    results = await asyncio.gather(
        async_task("任务1", 2),
        async_task("任务2", 2),
        async_task("任务3", 2),
    )

    end = time.time()
    print(f"异步总耗时: {end - start:.2f}秒")  # 约2秒
    return results

# ==================== 运行异步代码 ====================

# 在 Python 3.7+ 中，可以使用 asyncio.run() 运行异步函数
if __name__ == "__main__":
    print("=== 同步执行 ===")
    run_sync_tasks()

    print("\n=== 异步执行 ===")
    asyncio.run(run_async_tasks())

# ==================== async/await 语法详解 ====================

# async def 定义协程函数
async def fetch_data(url: str) -> dict:
    """模拟异步获取数据"""
    print(f"开始获取: {url}")
    await asyncio.sleep(1)  # 模拟网络请求
    return {"url": url, "data": "some data"}

# await 等待异步操作完成
async def process_data():
    """处理数据"""
    # 等待单个任务
    result = await fetch_data("https://api.example.com/data")
    print(f"获取到: {result}")

    # 等待多个任务
    tasks = [
        fetch_data("https://api.example.com/1"),
        fetch_data("https://api.example.com/2"),
        fetch_data("https://api.example.com/3"),
    ]
    results = await asyncio.gather(*tasks)
    print(f"批量获取: {len(results)}条数据")

# ==================== 异步上下文管理器 ====================

class AsyncDatabase:
    """模拟异步数据库连接"""

    async def connect(self):
        """异步连接"""
        print("连接数据库...")
        await asyncio.sleep(0.5)
        print("连接成功")

    async def disconnect(self):
        """异步断开"""
        print("断开数据库...")
        await asyncio.sleep(0.5)
        print("已断开")

    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.disconnect()

async def use_database():
    """使用异步上下文管理器"""
    async with AsyncDatabase() as db:
        print("使用数据库...")
        await asyncio.sleep(1)

# ==================== 异步迭代器 ====================

class AsyncCounter:
    """异步计数器"""

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.current = start

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= self.end:
            raise StopAsyncIteration
        self.current += 1
        await asyncio.sleep(0.1)  # 模拟异步操作
        return self.current - 1

async def use_async_iterator():
    """使用异步迭代器"""
    async for num in AsyncCounter(0, 5):
        print(f"计数: {num}")

# ==================== 实际应用：模拟 API 请求 ====================

async def mock_api_call(endpoint: str, delay: float = 1.0) -> dict:
    """模拟 API 调用"""
    print(f"请求: {endpoint}")
    await asyncio.sleep(delay)  # 模拟网络延迟
    return {"endpoint": endpoint, "status": "success"}

async def fetch_all_data():
    """并发获取多个 API 数据"""
    endpoints = [
        "/api/users",
        "/api/posts",
        "/api/comments",
    ]

    # 创建任务列表
    tasks = [mock_api_call(ep) for ep in endpoints]

    # 并发执行所有任务
    results = await asyncio.gather(*tasks)

    return results

# ==================== 为什么 FastAPI 使用异步 ====================
# 1. 高并发：同时处理多个请求
# 2. 非阻塞：等待 I/O 时不浪费 CPU
# 3. 高性能：比同步框架更快

# FastAPI 中的异步路由
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     # 这里可以使用 await 调用异步函数
#     item = await database.get_item(item_id)
#     return item

# ==================== 练习题 ====================
print("\n" + "="*50)
print("练习题：")
print("="*50)

# 练习1: 创建异步函数
# 编写 async def countdown(name, seconds)
# 每秒打印一次倒计时

# 在这里写你的代码：
# async def countdown(name: str, seconds: int):
#     ...

# 练习2: 并发执行
# 编写 async def run_multiple_tasks()
# 同时运行3个倒计时任务

# 在这里写你的代码：
# async def run_multiple_tasks():
#     ...

# 练习3: 异步数据处理
# 编写 async def process_items(items: List[str])
# 对每个项目模拟异步处理（await asyncio.sleep(0.5)）
# 返回处理结果列表

# 在这里写你的代码：
# async def process_items(items: List[str]) -> List[str]:
#     ...
