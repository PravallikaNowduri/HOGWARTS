@echo off
REM GryffinTwin Setup & Run Script for Windows

echo.
echo 🏰 GryffinTwin - Financial Management System
echo ===========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed
echo.

REM Start server
echo 🚀 Starting GryffinTwin backend...
echo.
echo Backend will run on: http://localhost:8000
echo API Docs available at: http://localhost:8000/docs
echo.
echo Open index.html in your browser to start using the app!
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
