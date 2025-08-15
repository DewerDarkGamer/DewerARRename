from PIL import Image
import cv2
import numpy as np
import os
import re
from pathlib import Path
import qrcode.image.svg

class BarcodeProcessor:
    """Class for processing images to extract barcode or QR code data using OpenCV"""

    def __init__(self):
        self.supported_formats = ['jpg', 'jpeg', 'JPG', 'JPEG']
        self.qr_detector = cv2.QRCodeDetector()
        self.barcode_detector = cv2.barcode_BarcodeDetector()

    def process_file(self, file_path):
        """
        Process a single file to extract barcode data

        Args:
            file_path (Path): Path to the image file

        Returns:
            dict: Processing result with success status and extracted data
        """
        try:
            # Open and process the image
            with Image.open(file_path) as image:
                if image.mode != 'RGB':
                    image = image.convert('RGB')

                cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                # 1) Try to detect QR code
                data, vertices_array, _ = self.qr_detector.detectAndDecode(cv_image)
                if data:
                    barcode_data = data
                    barcode_type = 'QRCODE'
                else:
                    # 2) Try to detect linear or other barcodes
                    ok, decoded_info, decoded_type, _ = self.barcode_detector.detectAndDecode(cv_image)
                    if ok and decoded_info and decoded_info[0]:
                        barcode_data = decoded_info[0]
                        barcode_type = decoded_type[0] if decoded_type else 'BARCODE'
                    else:
                        return {
                            'success': False,
                            'error': 'ไม่พบบาร์โค้ดหรือ QR โค้ดในรูปภาพ',
                            'barcode_data': None,
                            'barcode_type': None,
                            'new_name': None
                        }

                new_name = self.generate_filename(barcode_data, file_path.suffix)

                return {
                    'success': True,
                    'error': None,
                    'barcode_data': barcode_data,
                    'barcode_type': barcode_type,
                    'new_name': new_name
                }

        except Exception as e:
            return {
                'success': False,
                'error': f'เกิดข้อผิดพลาดในการประมวลผล: {str(e)}',
                'barcode_data': None,
                'barcode_type': None,
                'new_name': None
            }

    def generate_filename(self, barcode_data, original_extension):
        """Generate a safe filename from barcode data"""
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', barcode_data)
        safe_name = re.sub(r'[^\w\-_.]', '_', safe_name)
        safe_name = re.sub(r'_+', '_', safe_name).strip('_')

        if not safe_name:
            safe_name = 'barcode_data'

        max_name_length = 240 - len(original_extension)
        if len(safe_name) > max_name_length:
            safe_name = safe_name[:max_name_length]

        return f"{safe_name}{original_extension}"

    def validate_image(self, file_path):
        """Check if file is a supported JPEG"""
        try:
            extension = file_path.suffix.lower().lstrip('.')
            if extension not in ['jpg', 'jpeg']:
                return False
            with Image.open(file_path) as image:
                image.verify()
            return True
        except Exception:
            return False

    def get_file_info(self, file_path):
        """Get basic file information"""
        try:
            stat = file_path.stat()
            return {
                'name': file_path.name,
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'modified': stat.st_mtime
            }
        except Exception:
            return None

    
def detect_linear_barcode(self, cv_image):
    """
    Detect any 1D/2D barcodes in the image using pyzbar
    """
    try:
        barcodes = decode(cv_image)
        if not barcodes:
            return None
        # คืนค่าข้อมูลของบาร์โค้ดแรกที่เจอ
        return barcodes[0].data.decode('utf-8')
    except Exception as e:
        print(f"Error in linear barcode detection: {e}")
        return None

    
    def extract_barcode_text_from_image(self, gray_image):
        """
        Extract barcode text from the entire image using OCR
        Looks for patterns that match common barcode formats
        
        Args:
            gray_image: Grayscale OpenCV image
            
        Returns:
            str: Detected barcode text or None
        """
        try:
            # Use OCR to extract all text from the image
            text = pytesseract.image_to_string(gray_image, config='--psm 6')
            
            if text:
                # Split text into lines and look for barcode patterns
                lines = text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    
                    # Remove asterisks that are common in barcode text
                    clean_line = line.replace('*', '').strip()
                    
                    # Look for alphanumeric patterns that look like barcode data
                    # Pattern: letters and numbers (like ARHZ43I03901)
                    pattern_matches = re.findall(r'[A-Z]{2,}[0-9I]{2,}[A-Z0-9I]*', clean_line)
                    if pattern_matches:
                        # Return the longest match (most likely to be barcode)
                        result = max(pattern_matches, key=len)
                        # Clean up common OCR mistakes (1 vs I)
                        if len(result) >= 8:
                            return result
                    
                    # Also look for patterns with numbers followed by letters
                    pattern_matches = re.findall(r'[A-Z0-9I]{8,}', clean_line)
                    if pattern_matches:
                        # Filter out common words and return barcode-like patterns
                        for match in pattern_matches:
                            if any(c.isdigit() for c in match):
                                return match
            
            return None
            
        except Exception as e:
            print(f"Error extracting barcode text from image: {e}")
            return None
    
    def extract_text_from_barcode_region(self, roi):
        """
        Extract text from a potential barcode region using OCR
        
        Args:
            roi: Region of interest (binary image)
            
        Returns:
            str: Extracted text or None
        """
        try:
            # Use OCR to extract text from the region
            text = pytesseract.image_to_string(roi, config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789*')
            
            if text:
                # Clean the text
                text = text.strip()
                # Remove asterisks that are common in barcode text
                text = text.replace('*', '')
                
                # Look for alphanumeric patterns that look like barcode data
                # Pattern: letters followed by numbers (like ARHZ43I03901)
                pattern = re.search(r'[A-Z0-9]{6,}', text)
                if pattern:
                    return pattern.group()
                    
                # If no clear pattern, return the cleaned text if it's reasonable length
                if 6 <= len(text) <= 20 and text.isalnum():
                    return text
            
            return None
            
        except Exception as e:
            print(f"Error extracting text with OCR: {e}")
            return None
