#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

echo "==============================================="
echo "Hand Drawing Project Setup - Mac"
echo "==============================================="
echo
echo "Running from: $(pwd)"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo
    echo "Please download and install Python from:"
    echo "https://www.python.org/downloads/"
    echo "OR"
    echo "Install using Homebrew: brew install python"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version)
echo "✓ $PYTHON_VERSION detected"
echo

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed!"
    echo "Please ensure Python was installed correctly."
    read -p "Press Enter to exit..."
    exit 1
fi

# Install required packages
echo "Installing required libraries..."
echo "This may take a few minutes..."
echo

pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Could not install required libraries."
    read -p "Press Enter to exit..."
    exit 1
fi

echo
echo "✓ All libraries installed successfully!"
echo

# Check if virtual_painter.py exists
if [ ! -f "virtual_painter.py" ]; then
    echo "ERROR: virtual_painter.py not found!"
    echo "Make sure all project files are in the same folder."
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Triggering camera permission prompt..."
python3 -c "import cv2; cap=cv2.VideoCapture(0); cap.read(); cap.release()"
echo
read -p "If you saw a camera permission popup, please click 'OK' and then press Enter to continue... For the second time, just press Enter to continue..."

echo "Starting the Hand Drawing application..."
echo
echo "Instructions:"
echo "- Show your hand to the camera"
echo "- Use your index finger to draw in the air"
echo "- Press 'esc' to quit"
echo

# Run the virtual painter application
python3 virtual_painter.py

if [ $? -ne 0 ]; then
    echo
    echo "Application ended with an error."
    read -p "Press Enter to exit..."
    exit 1
fi

echo
echo "Application closed successfully! You can now close this terminal window."
exit 0