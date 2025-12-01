@echo off
echo ==========================================
echo      Music Recommender Setup Script
echo ==========================================

REM Check for Python 3.11
py -3.11 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.11 is not installed or not found in PATH.
    echo Please install it from: https://www.python.org/downloads/release/python-3119/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [1/4] Found Python 3.11. Cleaning up old environment...
if exist venv (
    rmdir /s /q venv
)

echo [2/4] Creating new virtual environment...
py -3.11 -m venv venv

echo [3/4] Activating environment...
call venv\Scripts\activate

echo [4/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo ==========================================
echo      Setup Complete! 
echo ==========================================
echo You can now run the app with:
echo    python main.py
echo.
pause
