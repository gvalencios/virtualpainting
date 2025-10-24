@echo off
chcp 65001 >nul

cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set pyversion=%%i
echo ✓ %pyversion% detected

pip install -r requirements.txt
if errorlevel 1 (
    pip3 install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Could not install required libraries.
        pause
        exit /b 1
    )
)

echo ✓ All libraries installed successfully!

if not exist "virtual_painter.py" (
    echo ERROR: virtual_painter.py not found!
    pause
    exit /b 1
)

python virtual_painter.py
if errorlevel 1 (
    echo ERROR: Could not run the virtual painter application.
    pause
    exit /b 1
)

pause
