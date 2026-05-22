@echo off
title Code Quest
set ROOT=%~dp0
cd /d %ROOT%

echo ========================================
echo      Code Quest - Python Learning
echo ========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found
    pause
    exit /b 1
)

if not exist "venv\Scripts\python.exe" (
    echo [SETUP] Creating venv...
    python -m venv venv
)

echo [SETUP] Installing backend deps...
"venv\Scripts\pip" install -r backend\requirements.txt -q

if not exist "frontend\node_modules" (
    echo [SETUP] Installing frontend deps...
    cd frontend
    call npm install
    cd ..
)

echo [INFO] Freeing up ports...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5174.*LISTENING"') do taskkill /f /pid %%a >nul 2>&1

echo.
echo [INFO] Starting backend on port 8000...
start "Backend" /min cmd /c "cd /d %ROOT% && set PYTHONPATH=%ROOT% && venv\Scripts\python -m uvicorn backend.main:app --port 8000"

echo [INFO] Starting frontend on port 5174...
start "Frontend" /min cmd /c "cd /d %ROOT%frontend && npm run dev"

echo [INFO] Waiting 8 seconds for servers to start...
timeout /t 8 /nobreak >nul

echo [INFO] Opening browser...
start http://localhost:5174

echo.
echo ========================================
echo   Backend:  http://localhost:8000/docs
echo   Frontend: http://localhost:5174
echo ========================================
echo.
echo You can close this window. Servers keep running.
pause >nul
