@echo off
chcp 65001 >nul

:: Change to the directory where the batch file is located
cd /d "%~dp0"

echo ===============================================
echo Hand Drawing Project Setup - Windows
echo ===============================================
echo.
echo Running from: %CD%
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please download and install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set pyversion=%%i
echo ✓ %pyversion% detected
echo.

:: Install required packages
echo Installing required libraries...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Trying with pip3...
    pip3 install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Could not install required libraries.
        echo Please check your internet connection and try again.
        pause
        exit /b 1
    )
)

echo.
echo ✓ All libraries installed successfully!
echo.

:: Run the main project file
echo Starting the Hand Drawing application...
echo.
echo Instructions:
echo - Show your hand to the camera
echo - Use your index finger to draw in the air
echo - Press 'esc' to quit
echo.
echo Please allow camera access when prompted...
echo.

python virtual_painter.py

if errorlevel 1 (
    echo.
    echo ERROR: Could not run the virtual painter application.
    echo Make sure all files are in the same folder.
    pause
    exit /b 1
)

pause