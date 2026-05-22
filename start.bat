@echo off
title Code Quest

echo ========================================
echo      Code Quest - Python Learning
echo ========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js
    pause
    exit /b 1
)

if not exist "venv\Scripts\python.exe" (
    echo [SETUP] Creating Python virtual environment...
    python -m venv venv
)

echo [SETUP] Checking backend dependencies...
"venv\Scripts\pip" install -r "backend\requirements.txt" -q

if not exist "frontend\node_modules" (
    echo [SETUP] Installing frontend dependencies (1-2 min first time)...
    cd frontend
    call npm install
    cd ..
)

echo.
echo [INFO] Starting backend on port 8000...
start "CodeQuest-Backend" cmd /c "cd /d "%cd%" && set PYTHONPATH=%cd% && "venv\Scripts\python" -m uvicorn backend.main:app --port 8000"

echo [INFO] Starting frontend on port 5174...
start "CodeQuest-Frontend" cmd /c "cd /d "%cd%\frontend" && npm run dev"

echo [INFO] Waiting for server to be ready (max 30s)...
set RETRY=0
:wait_loop
timeout /t 2 /nobreak >nul
set /a RETRY+=1
powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:5174' -TimeoutSec 2; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 goto browser_open
if %RETRY% lss 15 (
    echo [INFO] Waiting... (%RETRY%/15)
    goto wait_loop
)

:browser_open
echo [INFO] Opening browser...
start "" http://localhost:5174

echo.
echo ========================================
echo   Backend:  http://localhost:8000/docs
echo   Frontend: http://localhost:5174
echo ========================================
echo.
echo You can close this window. Servers will keep running.
pause >nul
