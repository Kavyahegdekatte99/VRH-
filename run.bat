@echo off
echo Starting VINAYAK REXINE HOUSE Catalog System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing/updating dependencies...
pip install -r requirements.txt

REM Run the application
echo.
echo Starting Flask application...
echo.
echo ========================================
echo   VINAYAK REXINE HOUSE - Catalog System
echo ========================================
echo.
echo Application will be available at:
echo http://localhost:5000
echo.
echo Admin Login: admin@rexinehouse.com / admin123
echo Note: Catalog starts empty - login as admin to add products
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause