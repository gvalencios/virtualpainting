#!/usr/bin/env python3
"""
Virtual Painter Project Launcher
Cross-platform setup and run script for Mac and Windows
"""

import os
import sys
import subprocess
import platform

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=" * 50)
    print("Hand Drawing Project Setup")
    print("=" * 50)
    print(f"\nRunning from: {os.getcwd()}")
    print(f"Platform: {platform.system()}\n")
    
    # Determine the correct Python 3.9 command
    python_cmd = find_python39()
    if not python_cmd:
        print("ERROR: Python 3.9 is not installed!")
        print("\nPlease download and install Python 3.9.x from:")
        print("https://www.python.org/downloads/")
        if platform.system() == "Darwin":
            print("OR install using Homebrew: brew install python@3.9")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Get Python version
    version = subprocess.check_output([python_cmd, "--version"], text=True).strip()
    print(f"✓ {version} detected\n")
    
    # Create virtual environment if it doesn't exist
    venv_path = os.path.join(script_dir, "venv")
    if not os.path.exists(venv_path):
        print("Creating virtual environment with Python 3.9...")
        result = subprocess.run([python_cmd, "-m", "venv", "venv"])
        if result.returncode != 0:
            print("ERROR: Could not create virtual environment")
            input("Press Enter to exit...")
            sys.exit(1)
        print("✓ Virtual environment created successfully!\n")
    else:
        print("✓ Virtual environment already exists\n")
    
    # Determine pip and python paths in venv
    if platform.system() == "Windows":
        venv_python = os.path.join(venv_path, "Scripts", "python.exe")
        venv_pip = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        venv_python = os.path.join(venv_path, "bin", "python")
        venv_pip = os.path.join(venv_path, "bin", "pip")
    
    # Install requirements
    print("Installing required libraries...")
    print("This may take a few minutes...\n")
    
    result = subprocess.run([venv_pip, "install", "-r", "requirements.txt"])
    if result.returncode != 0:
        print("\nERROR: Could not install required libraries.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("\n✓ All libraries installed successfully!\n")
    
    # Check if virtual_painter.py exists
    if not os.path.exists("virtual_painter.py"):
        print("ERROR: virtual_painter.py not found!")
        print("Make sure all project files are in the same folder.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Trigger camera permission on Mac
    if platform.system() == "Darwin":
        print("Triggering camera permission prompt...")
        subprocess.run([venv_python, "-c", 
                       "import cv2; cap=cv2.VideoCapture(0); cap.read(); cap.release()"])
        input("\nIf you saw a camera permission popup, please click 'Allow' and press Enter to continue, else just press Enter...\n")
    
    print("Starting the Hand Drawing application...\n")
    print("Instructions:")
    print("- Show your hand to the camera")
    print("- Use your index finger to draw in the air")
    print("- Press 'esc' to quit\n")
    
    # Run the virtual painter application
    result = subprocess.run([venv_python, "virtual_painter.py"])
    
    if result.returncode != 0:
        print("\nApplication ended with an error.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("\nApplication closed successfully!")
    if platform.system() == "Windows":
        input("Press Enter to exit...")

def find_python39():
    """Find Python 3.9 executable"""
    # Try different command variations
    commands = []
    
    if platform.system() == "Windows":
        commands = ["py -3.9", "python3.9", "python"]
    else:
        commands = ["python3.9", "python3"]
    
    for cmd in commands:
        try:
            cmd_parts = cmd.split()
            result = subprocess.run(
                cmd_parts + ["--version"],
                capture_output=True,
                text=True
            )
            version_output = result.stdout + result.stderr
            if "3.9" in version_output:
                return cmd_parts[0] if len(cmd_parts) == 1 else cmd
        except:
            continue
    
    return None

if __name__ == "__main__":
    main()
