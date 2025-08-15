#!/usr/bin/env python3
"""
Build script to create executable using PyInstaller
"""

import os
import subprocess
import sys
from pathlib import Path

def build_executable():
    """Build the executable using PyInstaller"""
    
    print("กำลังสร้างไฟล์ .exe...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create single executable file
        "--console",                    # Show console window (for debugging)
        "--name=JPG_Barcode_Renamer",   # Name of the executable
        "--add-data=app.py:.",          # Include app.py
        "--add-data=barcode_processor.py:.",  # Include barcode_processor.py
        "--add-data=.streamlit:.streamlit",   # Include Streamlit config
        "--hidden-import=streamlit",    # Ensure Streamlit is included
        "--hidden-import=cv2",          # Ensure OpenCV is included
        "--hidden-import=PIL",          # Ensure PIL is included
        "--hidden-import=pandas",       # Ensure pandas is included
        "--hidden-import=numpy",        # Ensure numpy is included
        "--hidden-import=qrcode",       # Ensure qrcode is included
        "--collect-all=streamlit",      # Collect all Streamlit files
        "--collect-all=cv2",            # Collect all OpenCV files
        "launcher.py"                   # Main script
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("สร้างไฟล์ .exe สำเร็จ!")
        print("ไฟล์ .exe อยู่ในโฟลเดอร์ 'dist/'")
        print("ชื่อไฟล์: JPG_Barcode_Renamer.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"เกิดข้อผิดพลาดในการสร้าง .exe: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False
    
    return True

if __name__ == "__main__":
    build_executable()