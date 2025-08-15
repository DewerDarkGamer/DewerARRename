#!/bin/bash

echo "Creating executable file for JPG Barcode Renamer..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python not found. Please install Python first."
    exit 1
fi

# Install required dependencies
echo "Installing required libraries..."
pip3 install tkinter opencv-python pandas pillow qrcode pyinstaller

# Create executable with PyInstaller
echo
echo "Creating executable file..."
pyinstaller --onefile --windowed --name=JPG_Barcode_Renamer \
    --add-data="desktop_app.py:." \
    --add-data="barcode_processor.py:." \
    --hidden-import=tkinter \
    --hidden-import=cv2 \
    --hidden-import=PIL \
    --hidden-import=pandas \
    --hidden-import=numpy \
    --hidden-import=qrcode \
    desktop_app.py

if [ -f "dist/JPG_Barcode_Renamer" ]; then
    echo
    echo "Executable file created successfully!"
    echo "File location: dist/JPG_Barcode_Renamer"
    echo
    echo "You can copy the executable file to other computers without Python installation"
else
    echo
    echo "Error occurred while creating executable file"
fi

echo
read -p "Press Enter to close..."