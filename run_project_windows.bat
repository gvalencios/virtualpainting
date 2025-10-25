@echo off

where py -3.9 >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.9 is not installed!
    echo Please install Python 3.9.6 or any 3.9.x version
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set pyversion=%%i
echo ✓ %pyversion% detected

if not exist "venv" (
    echo Creating virtual environment with Python 3.9...
    py -3.9 -m venv venv
    if errorlevel 1 (
        echo ERROR: Could not create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created successfully!
) else (
    echo ✓ Virtual environment already exists
)

call venv\Scripts\activate.bat

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
