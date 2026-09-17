@echo off

echo ==========================================
echo Network Infrastructure Monitoring
echo ==========================================

echo.
echo [1/3] Detecting local network...
python setup_network.py

if errorlevel 1 (
    echo Failed to detect network configuration.
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Windows network agent...

start "Network Agent" cmd /k "python host_network_agent.py"

timeout /t 2 /nobreak >nul

echo.
echo [3/3] Starting Docker services...

docker compose up -d

if errorlevel 1 (
    echo Failed to start Docker services.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Dashboard is running!
echo ==========================================
echo.
echo Dashboard: http://localhost
echo Grafana:   http://localhost:3000
echo Prometheus: http://localhost:9090
echo.
pause