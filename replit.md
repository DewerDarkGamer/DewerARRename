# JPG Barcode Renamer

## Overview

This is a Streamlit-based web application designed to rename JPG image files by extracting barcode data from the images. The application scans JPG files in a specified folder, reads barcode information from each image, and provides functionality to rename files based on the extracted barcode data. The app features a Thai language interface and is built for ease of use with a web-based GUI.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for web-based GUI
- **Layout**: Wide layout configuration for better file management display
- **State Management**: Streamlit session state to persist user selections and processing results
- **User Interface**: Thai language interface with emoji icons for visual appeal
- **Components**: File path input, folder validation, and processing results display

### Backend Architecture
- **Core Processing**: Modular design with separate `BarcodeProcessor` class
- **Image Processing**: PIL (Python Imaging Library) for image handling and format conversion
- **Barcode Detection**: pyzbar library for decoding various barcode formats
- **File Operations**: pathlib and os modules for cross-platform file system operations
- **Error Handling**: Comprehensive error handling for file access and barcode processing

### Data Flow
- User inputs folder path through web interface
- Application validates folder existence and accessibility
- System scans for supported image formats (JPG, JPEG)
- Each image is processed to extract barcode data
- Results are stored in session state for persistence
- User can preview changes before applying file renames

### File Processing Strategy
- **Supported Formats**: JPG and JPEG files (case-insensitive)
- **Image Conversion**: Automatic RGB conversion for compatibility
- **Barcode Extraction**: Multi-format barcode support through pyzbar
- **Filename Generation**: Custom logic to create new filenames from barcode data
- **Batch Processing**: Handles multiple files in a single operation

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **PIL (Pillow)**: Image processing and manipulation library
- **pyzbar**: Barcode and QR code detection and decoding library
- **pandas**: Data manipulation and analysis (for results display)
- **pathlib**: Modern path handling utilities

### System Requirements
- Python environment with image processing capabilities
- Access to local file system for reading and renaming files
- Support for various barcode formats through pyzbar

### Optional Integrations
- File system permissions for reading and writing operations
- Cross-platform compatibility for Windows and Unix-like systems

## Recent Changes (August 15, 2025)

### Executable Creation Support
- **Added PyInstaller Integration**: Created build scripts to convert the Streamlit app into standalone .exe files
- **Cross-Platform Build Scripts**: 
  - `create_exe.bat` for Windows users
  - `create_exe.sh` for Mac/Linux users
  - `launcher.py` as the main entry point for compiled executables
- **Build Process**: Automated script that handles dependency installation and PyInstaller compilation
- **Distribution Ready**: Generated executables can run without Python installation on target machines

### Library Migration
- **Switched from pyzbar to OpenCV**: Due to Replit environment limitations with zbar library
- **QR Code Focus**: Currently supports QR codes specifically (most common barcode type)
- **Maintained Functionality**: Core features remain the same despite library change

### User Preferences Updates
- **Executable Distribution**: User requested .exe file creation for easier distribution
- **Simplified Deployment**: Focus on creating standalone applications that don't require technical setup