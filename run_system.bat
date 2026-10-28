@echo off
title Face Recognition Attendance System
echo.
echo ========================================
echo   Face Recognition Attendance System
echo ========================================
echo.
echo Starting the system launcher...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "face_attendance_env\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv face_attendance_env
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment and install packages
echo Activating virtual environment...
call face_attendance_env\Scripts\activate.bat

REM Check if packages are installed
python -c "import cv2, numpy, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install packages
        pause
        exit /b 1
    )
)

echo.
echo Starting the system...
echo.

REM Run the launcher
python run_system.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo An error occurred. Press any key to exit...
    pause >nul
)




