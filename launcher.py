#!/usr/bin/env python3
"""
Launcher script for JPG Barcode Renamer
This script launches the Streamlit app in a way that's compatible with PyInstaller
"""

import sys
import os
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def find_free_port():
    """Find a free port to run the app"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def launch_streamlit():
    """Launch the Streamlit app"""
    try:
        # Get the directory where the executable is located
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            app_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Change to app directory
        os.chdir(app_dir)
        
        # Find free port
        port = find_free_port()
        
        print(f"กำลังเริ่มต้น JPG Barcode Renamer...")
        print(f"แอปจะเปิดในเบราว์เซอร์ที่พอร์ต {port}")
        
        # Start Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "app.py", 
            "--server.port", str(port),
            "--server.address", "localhost",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ]
        
        # Start Streamlit in a separate process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Open browser
        url = f"http://localhost:{port}"
        print(f"เปิดเบราว์เซอร์ที่: {url}")
        webbrowser.open(url)
        
        # Keep the process running
        print("กดปุ่ม Ctrl+C เพื่อปิดแอป")
        try:
            process.wait()
        except KeyboardInterrupt:
            print("กำลังปิดแอป...")
            process.terminate()
            process.wait()
            
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        input("กดปุ่ม Enter เพื่อปิด...")

if __name__ == "__main__":
    launch_streamlit()