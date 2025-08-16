#!/usr/bin/env python3
"""
Build script to create executable using PyInstaller
"""

import os
import subprocess
import sys
from pathlib import Path
import shutil

def check_requirements():
    """Check if all required files and directories exist"""
    required_files = ['app.py', 'barcode_processor.py', 'launcher.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"ไฟล์ที่จำเป็นไม่พบ: {', '.join(missing_files)}")
        return False
    
    # Create .streamlit directory if it doesn't exist
    if not os.path.exists('.streamlit'):
        os.makedirs('.streamlit')
        print("สร้างโฟลเดอร์ .streamlit")
    
    return True

def build_with_spec():
    """Build using spec file approach"""
    print("กำลังสร้างไฟล์ .exe ด้วย spec file...")
    
    cmd = ["pyinstaller", "--clean", "JPG_Barcode_Renamer.spec"]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"การ build ด้วย spec file ล้มเหลว: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def build_direct():
    """Build directly with pyinstaller command"""
    print("กำลังสร้างไฟล์ .exe ด้วยคำสั่งโดยตรง...")
    
    # Clear previous build
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # PyInstaller command for desktop app
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name=JPG_Barcode_Renamer_Desktop",
        "--hidden-import=tkinter",
        "--hidden-import=cv2", 
        "--hidden-import=PIL",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=pyzbar.pyzbar",
        "--add-data=barcode_processor.py:.",
        "desktop_app.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("สร้าง Desktop App .exe สำเร็จ!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"การ build Desktop app ล้มเหลว: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def build_streamlit_launcher():
    """Build Streamlit launcher executable"""
    print("กำลังสร้างไฟล์ .exe สำหรับ Streamlit launcher...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console", 
        "--name=JPG_Barcode_Renamer_Web",
        "--add-data=app.py:.",
        "--add-data=barcode_processor.py:.",
        "--add-data=.streamlit:.streamlit",
        "--hidden-import=streamlit",
        "--hidden-import=cv2",
        "--hidden-import=PIL", 
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=pyzbar.pyzbar",
        "--collect-all=streamlit",
        "launcher.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("สร้าง Streamlit launcher .exe สำเร็จ!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"การ build Streamlit launcher ล้มเหลว: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def build_executable():
    """Main build function"""
    print("=== JPG Barcode Renamer Executable Builder ===")
    print()
    
    # Check requirements
    if not check_requirements():
        return False
    
    success_count = 0
    
    # Try building desktop app
    if build_direct():
        success_count += 1
        print("✅ Desktop App executable สร้างสำเร็จ")
    else:
        print("❌ Desktop App executable สร้างไม่สำเร็จ")
    
    print()
    
    # Try building Streamlit launcher
    if build_streamlit_launcher():
        success_count += 1  
        print("✅ Streamlit Web App launcher สร้างสำเร็จ")
    else:
        print("❌ Streamlit Web App launcher สร้างไม่สำเร็จ")
    
    print()
    print("=== สรุปผลการ Build ===")
    
    if success_count > 0:
        print(f"สร้างไฟล์ .exe สำเร็จ {success_count} ไฟล์")
        print("ไฟล์ .exe อยู่ในโฟลเดอร์ 'dist/'")
        
        # List created files
        if os.path.exists('dist'):
            exe_files = [f for f in os.listdir('dist') if f.endswith('.exe')]
            for exe_file in exe_files:
                print(f"  - {exe_file}")
        
        print()
        print("หมายเหตุ:")
        print("- JPG_Barcode_Renamer_Desktop.exe = แอป Desktop (tkinter)")
        print("- JPG_Barcode_Renamer_Web.exe = แอป Web (Streamlit)")
        return True
    else:
        print("ไม่สามารถสร้างไฟล์ .exe ใดๆ ได้")
        print("กรุณาตรวจสอบ error messages ข้างต้น")
        return False

if __name__ == "__main__":
    success = build_executable()
    if not success:
        input("กด Enter เพื่อปิด...")
    else:
        print("\nการ build เสร็จสิ้น!")
