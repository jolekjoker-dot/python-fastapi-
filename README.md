# Code Quest — 交互式 Python 学习平台

将枯燥的编程学习变成 RPG 闯关游戏。你扮演魔法学徒，通过完成 25 个关卡学习 Python、FastAPI 和全栈开发。

---

## 项目架构

```
fastapi/
├── backend/                    # FastAPI 后端
│   ├── main.py                 # 应用入口
│   ├── config.py               # 配置（DB路径、JWT密钥、沙箱设置）
│   ├── database.py             # SQLAlchemy + SQLite
│   ├── models/                 # 数据表：User, Progress, ExecutionHistory
│   ├── schemas/                # Pydantic 校验模型
│   ├── routers/                # API 路由（auth/quests/execute/persistence/game）
│   ├── services/               # 业务逻辑（认证/沙箱/关卡/游戏化）
│   ├── sandbox/                # AST 安全检查
│   ├── data/quests/            # 25 关课程 JSON 数据
│   └── code_quest.db           # SQLite 数据库（自动创建）
├── frontend/                   # React 前端
│   └── src/
│       ├── pages/              # 页面：Login/Map/Quest/Achievements/Shop/Leaderboard
│       ├── components/         # 组件：CodeEditor/TopNav/ResizeHandle/Confetti
│       ├── hooks/              # usePanelResize / useWindowSize
│       ├── api/                # API 调用层
│       └── stores/             # Zustand 状态管理
├── start.bat                   # Windows 一键启动脚本
├── phase1_basics/              # 原始 Python 学习资料（参考用）
└── phase2_fastapi/             # 原始 FastAPI 学习资料（参考用）
```

---

## 25 关课程总览

### 第一篇章：学徒试炼 — Python 基础（关卡 1-10）

| 关卡 | 标题 | 核心知识点 |
|:---:|------|----------|
| 1 | 变量与数据类型 | int, str, float, bool, f-string, type(), 类型转换 |
| 2 | 条件判断 | if/elif/else, 比较运算符, and/or/not |
| 3 | for/while 循环 | for, while, range(), break/continue, 列表推导式 |
| 4 | 函数 | def, 参数, 默认参数, return, *args |
| 5 | 类与对象 | class, __init__, self, 方法, 继承, super() |
| 6 | 集合类型 | list 操作, dict 操作, set 去重, 字典推导式, 切片 |
| 7 | 异常处理 | try/except/finally, ValueError, KeyError, 自定义异常 |
| 8 | 类型提示 | 类型注解, Optional, list[int], dataclass |
| 9 | 异步基础 | async/await, asyncio.gather(), 并发 vs 同步 |
| 10 | 🏰 Boss 战 | 综合：Student + Academy 管理系统 |

### 第二篇章：魔法阵构筑 — FastAPI（关卡 11-18）

| 关卡 | 标题 | 核心知识点 |
|:---:|------|----------|
| 11 | Hello FastAPI | FastAPI(), @app.get(), uvicorn, 路径参数, 查询参数 |
| 12 | 路由与请求处理 | 路径参数类型转换, 查询参数, POST 请求体, Pydantic 模型 |
| 13 | 响应处理 | status_code, response_model, HTTPException, 404/400 |
| 14 | Pydantic 深度 | Field() 约束, Enum 枚举, 嵌套模型, 数据校验 |
| 15 | Todo CRUD（上） | 内存存储, GET/POST, 过滤查询, 单个查询 |
| 16 | Todo CRUD（下） | PUT 更新, DELETE 删除, PATCH 部分更新, 批量操作 |
| 17 | 项目重构 | APIRouter 拆分, Depends 依赖注入, CORS 中间件 |
| 18 | 🏰 Boss 战 | 综合 CRUD API + 搜索 + 批量操作 |

### 第三篇章：神器锻造 — 全栈实战（关卡 19-25）

| 关卡 | 标题 | 核心知识点 |
|:---:|------|----------|
| 19 | SQLite + SQLAlchemy | ORM 模型, create_engine, Session CRUD, 模糊搜索 |
| 20 | JWT 用户认证 | bcrypt 密码哈希, JWT 签发/验证, HTTPBearer, 受保护路由 |
| 21 | React CDN 入门 | CDN 引入 React, useState, JSX, 事件处理, 组件 |
| 22 | API 客户端实战 | APIClient 类封装, urllib, 错误处理, 类型注解 |
| 23 | Prism.js 代码高亮 | CDN 引入, 多语言, 行号插件, 自定义样式 |
| 24 | 游戏化系统 API | XP 计算, 成就检测, 打卡系统, 连续天数 |
| 25 | 🏰 Boss 战 | Dockerfile + docker-compose.yml 编写 |

---

## 关卡设计

### 每关结构

```json
{
  "id": "quest_01",
  "title": "觉醒之刻 — 变量与数据类型",
  "phase": 1,
  "order": 1,
  "xp_reward": 100,
  "story": "NPC 对话（Markdown）",
  "content": "知识点教程（Markdown，含代码示例）",
  "tasks": [
    {
      "id": "task_01",
      "description": "任务描述（Markdown）",
      "starter_code": "编辑器初始代码",
      "test_cases": [{ "type": "output_match", "expected": "...", "description": "..." }],
      "hints": ["提示1", "提示2"]
    }
  ],
  "challenge": { "id": "challenge_01", "..." }
}
```

### 关卡组成

每关包含 **3 个交互任务** + **1 个挑战题**。完成全部任务和挑战后获得 XP 和金币。

### 解锁规则

顺序解锁：完成第 N 关后，第 N+1 关自动解锁。

---

## 三种代码执行引擎

| 引擎 | 测试类型 | 用途 | 工作流程 |
|------|:---:|------|----------|
| `code_executor` | `output_match` / `output_contains` | Python 基础 (1-10)、Docker (25) | 写入 `.py` → subprocess 执行 → 比对 stdout |
| `fastapi_executor` | `http_test` | FastAPI (11-18)、SQLAlchemy (19-20)、游戏化 API (24) | 写入临时目录 → 启动 uvicorn → HTTP 请求测试 → 杀进程 |
| `frontend_executor` | `html_check` | React (21)、Prism.js (23) | 写入 `index.html` → 启动 http.server → 检查页面源码 |

---

## 界面展示

### 登录页
- 输入法师名即可进入（无需密码）
- 首次输入自动注册，再次输入自动登录

### 关卡地图 `/map`
- 三大篇章分区显示，每关一个方块节点
- 方块状态：✅已通关（绿色）/ Ready（金色脉冲）/ 🔒锁定（灰色）
- 方块间用彩色连线连接（通关后变绿）
- Boss 关以 👑 图标标识

### 关卡详情 `/quest/:id`
- **左侧面板**：NPC 故事对话 + 知识点教程 + 任务描述（Markdown 渲染）+ 任务导航标签 + 提示按钮
- **中间面板**：Monaco Editor 代码编辑器（语法高亮 + 自动补全 + Ctrl+Enter 运行）
- **右侧面板**：双 Tab 切换 — Results（测试结果 PASS/FAIL + 逐条期望值对比） / History（历史运行记录，点击可恢复代码）
- 三栏宽度可拖拽调整

### 成就殿堂 `/achievements`
- 10 种成就徽章，已解锁亮色 / 未解锁灰色 + 🔒
- GitHub 热力图风格打卡日历（最近 84 天）
- 点击打卡按钮记录每日学习

### 魔法商店 `/shop`
- 4 种商品：额外提示(50) / 暗夜主题(300) / 金色称号(500) / 跳过券(200)
- 已购买商品显示绿色边框 + "已拥有"标签
- 金币不足时按钮禁用

### 排行榜 `/leaderboard`
- 按 XP 排名，前 3 名显示 🥇🥈🥉
- 当前用户行高亮金色边框 + "(你)" 标记

### 顶部导航栏
- Code Quest 标题（点击回地图）
- Map / Achievements / Shop / Leaderboard 快捷按钮
- 等级 + XP 进度条（金色渐变，动画过渡）
- 金币数 + 用户名 + Exit 按钮

---

## 游戏化系统

| 系统 | 说明 |
|------|------|
| **XP / 等级** | 完成关卡 + 成就奖励，每 1000 XP 升一级 |
| **10 种成就** | 初出茅庐 / 见习法师 / 学霸之证 / Python大师 / 魔法阵构筑者 / 全栈大法师 / 闪电施法 / 百发百中 / 勤学苦练 / 代码工匠 |
| **打卡** | 每日打卡，连续天数统计，可视化热力图 |
| **金币商店** | 完成任务赚金币，购买提示/皮肤/称号/跳过券 |
| **通关撒花** | Canvas 粒子动画，彩色纸屑爆炸效果 |

---

## 数据持久化

所有用户数据存储在本地 SQLite（`backend/code_quest.db`）：

| 数据 | 表 | 说明 |
|------|-----|------|
| 用户信息 | `users` | 昵称、XP、等级、金币 |
| 关卡进度 | `progress` | 已完成的关卡和任务 |
| 运行历史 | `execution_history` | 每次提交的代码和结果 |
| 代码草稿 | `code_drafts` | 编辑器自动保存（2 秒防抖） |
| 偏好设置 | `user_preferences` | 面板宽度、成就、打卡、商店 |

---

## 技术栈

| 层 | 技术 |
|----|------|
| 后端框架 | FastAPI 0.136 |
| ORM | SQLAlchemy 2.0 (async) |
| 数据库 | SQLite (aiosqlite) |
| 认证 | PyJWT (无密码模式) |
| 前端框架 | React 18 + TypeScript |
| 构建工具 | Vite 8 |
| CSS | Tailwind CSS 4 |
| 代码编辑器 | Monaco Editor |
| 状态管理 | Zustand |
| Markdown | react-markdown |
| 动画 | Canvas Confetti (自研) |

---

## 快速开始

### 方式一：一键启动（推荐）

双击 `start.bat`，自动完成：创建虚拟环境 → 安装依赖 → 启动后端(8000) → 启动前端(5174) → 打开浏览器。

### 方式二：手动启动

```bash
# 1. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 2. 安装后端依赖
pip install -r backend/requirements.txt

# 3. 启动后端
set PYTHONPATH=%cd%
uvicorn backend.main:app --port 8000

# 4. 新终端，安装前端依赖
cd frontend
npm install

# 5. 启动前端
npm run dev
```

浏览器访问 `http://localhost:5174`

---

## 如何新增章节

### 1. 添加关卡

在 `backend/data/quests/` 下创建 `quest_26.json`，设置 `phase: 4` 即可。关卡地图会自动渲染新篇章。

### 2. 新增测试引擎（如需）

如果新章节需要特殊验证（如 SQL 执行、Redis 命令），仿照 `backend/services/fastapi_executor.py` 创建新执行器，在 `quest_service.py` 中添加新的 `type` 分支。

### 3. 关卡数据格式

参考上文 [关卡设计](#关卡设计) 部分的 JSON 结构。三种测试类型开箱可用：
- `output_match` / `output_contains` — 纯 Python 输出比对
- `http_test` — FastAPI HTTP 请求测试
- `html_check` — 前端页面源码检查

---

## Git 版本历史

查看 [CHANGELOG.md](CHANGELOG.md) 获取完整提交记录。
