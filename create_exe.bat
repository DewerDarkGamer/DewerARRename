@echo off
echo Creating .exe file for JPG Barcode Renamer...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Install required dependencies
echo Installing required libraries...
pip install tkinter opencv-python pandas pillow qrcode pyinstaller

REM Create .exe with PyInstaller
echo.
echo Creating .exe file...
pyinstaller --onefile --windowed --name=JPG_Barcode_Renamer --add-data="desktop_app.py;." --add-data="barcode_processor.py;." --hidden-import=tkinter --hidden-import=cv2 --hidden-import=PIL --hidden-import=pandas --hidden-import=numpy --hidden-import=qrcode desktop_app.py

if exist "dist\JPG_Barcode_Renamer.exe" (
    echo.
    echo .exe file created successfully!
    echo File location: dist\JPG_Barcode_Renamer.exe
    echo.
    echo You can copy the .exe file to other computers without Python installation
) else (
    echo.
    echo Error occurred while creating .exe file
)

echo.
pause