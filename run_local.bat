@echo off
echo ===============================================================================
echo            TRAIT INNOVATION - TRAIT AVIATION INTELLIGENCE v2.0
echo            Integrated AirportAI and Aviation Analytics Platform
echo ===============================================================================
echo.
echo [1/3] Verifying Python Environment...
python --version
if errorlevel 1 (
    echo [ERROR] Python 3.11 is required. Please install Python from python.org.
    pause
    exit /b 1
)

echo.
echo [2/3] Seeding Initial Synthetic Database...
cd backend
python -m app.seed_data

echo.
echo [3/3] Launching Full-Stack Application on http://127.0.0.1:8000 ...
echo Press Ctrl+C in this window to stop the server.
echo.
start http://127.0.0.1:8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
