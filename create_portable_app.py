#!/usr/bin/env python3
"""
สร้าง Portable Application สำหรับ JPG Barcode Renamer
เนื่องจาก PyInstaller มีปัญหาใน Replit environment
เราจะสร้าง portable app ที่ใช้งานได้โดยไม่ต้อง compile
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_portable_package():
    """สร้าง portable package"""
    
    print("=== สร้าง Portable Application Package ===")
    print()
    
    # สร้างโฟลเดอร์ dist ถ้ายังไม่มี
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # สร้างโฟลเดอร์สำหรับ portable app
    portable_dir = dist_dir / "JPG_Barcode_Renamer_Portable"
    portable_dir.mkdir()
    
    # ไฟล์ที่ต้องการ copy
    required_files = [
        "app.py",
        "desktop_app.py", 
        "barcode_processor.py",
        "launcher.py",
        "pyproject.toml"
    ]
    
    # Copy ไฟล์หลัก
    print("กำลัง copy ไฟล์หลัก...")
    for file in required_files:
        if os.path.exists(file):
            shutil.copy2(file, portable_dir)
            print(f"  ✓ {file}")
        else:
            print(f"  ⚠️ ไม่พบไฟล์: {file}")
    
    # Copy โฟลเดอร์ .streamlit
    streamlit_dir = Path(".streamlit")
    if streamlit_dir.exists():
        shutil.copytree(streamlit_dir, portable_dir / ".streamlit")
        print(f"  ✓ .streamlit/")
    
    # สร้างไฟล์ batch สำหรับ Windows
    create_windows_launcher(portable_dir)
    
    # สร้างไฟล์ shell script สำหรับ Linux/Mac
    create_unix_launcher(portable_dir)
    
    # สร้างไฟล์ README
    create_readme(portable_dir)
    
    # สร้างไฟล์ requirements
    create_requirements(portable_dir)
    
    # สร้างไฟล์ zip
    create_zip_package(dist_dir, portable_dir)
    
    print()
    print("=== สร้าง Portable Package สำเร็จ! ===")
    print(f"📁 โฟลเดอร์: {portable_dir}")
    print(f"📦 ไฟล์ ZIP: {dist_dir / 'JPG_Barcode_Renamer_Portable.zip'}")
    print()
    print("วิธีใช้งาน:")
    print("1. ดาวน์โหลดและแตกไฟล์ ZIP")
    print("2. ติดตั้ง Python และ dependencies ด้วย requirements.txt")
    print("3. รันไฟล์ .bat (Windows) หรือ .sh (Linux/Mac)")

def create_windows_launcher(portable_dir):
    """สร้างไฟล์ launcher สำหรับ Windows"""
    
    # Desktop App Launcher
    desktop_bat = portable_dir / "run_desktop_app.bat"
    with open(desktop_bat, 'w', encoding='utf-8') as f:
        f.write("""@echo off
echo ==================================================
echo    JPG Barcode Renamer - Desktop Application
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python first.
    echo Download from: https://python.org
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing dependencies...
pip install -r requirements.txt

REM Run desktop app
echo.
echo Starting Desktop Application...
python desktop_app.py

pause
""")
    
    # Web App Launcher
    web_bat = portable_dir / "run_web_app.bat"
    with open(web_bat, 'w', encoding='utf-8') as f:
        f.write("""@echo off
echo ==================================================
echo    JPG Barcode Renamer - Web Application
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python first.
    echo Download from: https://python.org
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing dependencies...
pip install -r requirements.txt

REM Run web app
echo.
echo Starting Web Application...
echo Your browser will open automatically...
python launcher.py

pause
""")
    
    print("  ✓ Windows launchers (.bat)")

def create_unix_launcher(portable_dir):
    """สร้างไฟล์ launcher สำหรับ Unix/Linux/Mac"""
    
    # Desktop App Launcher
    desktop_sh = portable_dir / "run_desktop_app.sh"
    with open(desktop_sh, 'w') as f:
        f.write("""#!/bin/bash

echo "=================================================="
echo "   JPG Barcode Renamer - Desktop Application"
echo "=================================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python not found. Please install Python first."
    exit 1
fi

# Install dependencies if needed
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Run desktop app
echo
echo "Starting Desktop Application..."
python3 desktop_app.py

read -p "Press Enter to close..."
""")
    
    # Web App Launcher  
    web_sh = portable_dir / "run_web_app.sh"
    with open(web_sh, 'w') as f:
        f.write("""#!/bin/bash

echo "=================================================="
echo "   JPG Barcode Renamer - Web Application"
echo "=================================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python not found. Please install Python first."
    exit 1
fi

# Install dependencies if needed
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Run web app
echo
echo "Starting Web Application..."
echo "Your browser will open automatically..."
python3 launcher.py

read -p "Press Enter to close..."
""")
    
    # Make executable
    os.chmod(desktop_sh, 0o755)
    os.chmod(web_sh, 0o755)
    
    print("  ✓ Unix/Linux launchers (.sh)")

def create_readme(portable_dir):
    """สร้างไฟล์ README"""
    
    readme_path = portable_dir / "README.txt"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("""
JPG Barcode Renamer - Portable Application
==========================================

คำอธิบาย:
---------
แอปพลิเคชันสำหรับเปลี่ยนชื่อไฟล์ JPG โดยใช้ข้อมูลบาร์โค้ดในรูปภาพ
รองรับการทำงานแบบ Desktop GUI และ Web Application

ความต้องการของระบบ:
------------------
- Python 3.8 หรือใหม่กว่า
- ระบบปฏิบัติการ: Windows, macOS, Linux

การติดตั้ง:
----------
1. ติดตั้ง Python จาก https://python.org
2. แตกไฟล์โปรแกรมลงในโฟลเดอร์ที่ต้องการ
3. เปิด Command Prompt/Terminal ในโฟลเดอร์โปรแกรม
4. รันคำสั่ง: pip install -r requirements.txt

วิธีใช้งาน:
----------

สำหรับ Windows:
- เปิด Desktop App: ดับเบิลคลิก run_desktop_app.bat  
- เปิด Web App: ดับเบิลคลิก run_web_app.bat

สำหรับ Mac/Linux:
- เปิด Desktop App: ./run_desktop_app.sh
- เปิด Web App: ./run_web_app.sh

หรือรันด้วยคำสั่ง Python โดยตรง:
- Desktop App: python desktop_app.py
- Web App: python launcher.py (หรือ streamlit run app.py)

คุณสมบัติ:
----------
- อ่านบาร์โค้ด/QR Code จากไฟล์ JPG
- เปลี่ยนชื่อไฟล์โดยอัตโนมัติตามข้อมูลบาร์โค้ด
- รองรับการทำงานแบบ Batch Processing
- อินเทอร์เฟซภาษาไทย
- รองรับหลายรูปแบบบาร์โค้ด

หมายเหตุ:
--------
- ตรวจสอบให้แน่ใจว่าโฟลเดอร์ที่มีไฟล์ JPG สามารถเข้าถึงได้
- สำรองข้อมูลก่อนเปลี่ยนชื่อไฟล์
- การเปลี่ยนชื่อไฟล์ไม่สามารถย้อนกลับได้

สนับสนุน:
---------
หากมีปัญหาการใช้งาน กรุณาตรวจสอบ:
1. Python ติดตั้งถูกต้องและอยู่ในค่า PATH
2. Dependencies ติดตั้งครบถ้วนด้วย requirements.txt
3. ไฟล์รูปภาพอยู่ในโฟลเดอร์ที่สามารถเข้าถึงได้

""")
    
    print("  ✓ README.txt")

def create_requirements(portable_dir):
    """สร้างไฟล์ requirements.txt"""
    
    requirements_path = portable_dir / "requirements.txt"
    with open(requirements_path, 'w') as f:
        f.write("""# JPG Barcode Renamer Dependencies
streamlit>=1.48.1
opencv-python>=4.12.0.88
pandas>=2.3.1
pillow>=11.3.0
pyzbar>=0.1.9
qrcode>=8.2
numpy>=2.2.6
""")
    
    print("  ✓ requirements.txt")

def create_zip_package(dist_dir, portable_dir):
    """สร้างไฟล์ ZIP package"""
    
    zip_path = dist_dir / "JPG_Barcode_Renamer_Portable.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in portable_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(dist_dir)
                zipf.write(file_path, arcname)
    
    print(f"  ✓ ZIP package: {zip_path.name}")

if __name__ == "__main__":
    create_portable_package()
