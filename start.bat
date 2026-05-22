@echo off
chcp 65001 >nul
title Code Quest - 学习平台

echo ========================================
echo      Code Quest - Python 学习冒险
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 未安装，请先安装 Python 3.11+
    pause
    exit /b 1
)

:: Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js 未安装，请先安装 Node.js
    pause
    exit /b 1
)

:: Create venv if needed
if not exist "venv\Scripts\python.exe" (
    echo [SETUP] 创建 Python 虚拟环境...
    python -m venv venv
)

:: Install backend dependencies
echo [SETUP] 检查后端依赖...
"venv\Scripts\pip" install -r "backend\requirements.txt" -q

:: Install frontend dependencies
if not exist "frontend\node_modules" (
    echo [SETUP] 安装前端依赖（首次需要 1-2 分钟）...
    cd frontend
    call npm install
    cd ..
)

echo.
echo [INFO] 启动后端服务 (端口 8000)...
start "CodeQuest-Backend" cmd /c "cd /d "%cd%" && set PYTHONPATH=%cd% && "venv\Scripts\python" -m uvicorn backend.main:app --port 8000"

echo [INFO] 启动前端服务 (端口 5174)...
start "CodeQuest-Frontend" cmd /c "cd /d "%cd%\frontend" && npm run dev"

echo [INFO] 等待服务就绪（最多 30 秒）...
set RETRY=0
:wait_loop
timeout /t 2 /nobreak >nul
set /a RETRY+=1
powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:5174' -TimeoutSec 2; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 goto browser_open
if %RETRY% lss 15 (
    echo [INFO] 等待中... (%RETRY%/15)
    goto wait_loop
)

:browser_open
echo [INFO] 打开浏览器...
start "" http://localhost:5174

echo.
echo ========================================
echo   后端: http://localhost:8000/docs
echo   前端: http://localhost:5174
echo ========================================
echo.
echo 按任意键关闭此窗口（不会影响已启动的服务）
pause >nul
