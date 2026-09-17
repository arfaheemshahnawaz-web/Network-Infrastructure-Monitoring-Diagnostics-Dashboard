@echo off
setlocal

cd /d "%~dp0"

title Network Infrastructure Monitoring

echo.
echo ==============================================
echo   Network Infrastructure Monitoring
echo ==============================================
echo.

REM ----------------------------------------------
REM Step 1 - Check Python
REM ----------------------------------------------

echo [1/5] Checking Python...

python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed.
    echo Please install Python 3.12 or later.
    echo.
    pause
    exit /b 1
)

echo Python detected.
echo.

REM ----------------------------------------------
REM Step 2 - Create virtual environment
REM ----------------------------------------------

echo [2/5] Checking virtual environment...

if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv

    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo Virtual environment ready.
echo.

REM ----------------------------------------------
REM Step 3 - Install dependencies
REM ----------------------------------------------

echo [3/5] Installing Python dependencies...

"venv\Scripts\python.exe" -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install Python dependencies.
    pause
    exit /b 1
)

echo Dependencies installed.
echo.

REM ----------------------------------------------
REM Step 4 - Detect network
REM ----------------------------------------------

echo [4/5] Detecting local network...

"venv\Scripts\python.exe" setup_network.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to detect local network.
    pause
    exit /b 1
)

echo Network configuration created.
echo.

REM ----------------------------------------------
REM Step 5 - Start services
REM ----------------------------------------------

echo [5/5] Starting services...

echo.
echo Starting Windows Network Agent...

start "Network Agent" cmd /k "cd /d ""%~dp0"" && ""%~dp0venv\Scripts\python.exe"" ""%~dp0host_network_agent.py"""

timeout /t 2 /nobreak >nul

echo.
echo Starting Docker services...

docker compose up --build -d --force-recreate

if errorlevel 1 (
    echo.
    echo ERROR: Docker services failed to start.
    echo Make sure Docker Desktop is running.
    pause
    exit /b 1
)

echo.
echo ==============================================
echo   Network Monitor Started Successfully!
echo ==============================================
echo.
echo Dashboard:  http://localhost
echo Grafana:    http://localhost:3000
echo Prometheus: http://localhost:9090
echo.
echo Network Agent: Running on port 8765
echo.
echo ==============================================

pause