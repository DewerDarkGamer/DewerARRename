import cv2
import os
from pyzxing import BarCodeReader

class BarcodeProcessor:
    def __init__(self):
        self.reader = BarCodeReader()

    def process_image(self, image_path):
        """
        อ่านบาร์โค้ดจากไฟล์ภาพ
        """
        if not os.path.exists(image_path):
            return None

        # ใช้ pyzxing อ่านบาร์โค้ด
        results = self.reader.decode(image_path)

        if not results:
            return None

        # คืนค่าข้อความแรกที่เจอ
        return results[0]['parsed']

    def process_folder(self, folder_path):
        """
        อ่านบาร์โค้ดจากทุกไฟล์ในโฟลเดอร์
        """
        if not os.path.exists(folder_path):
            return []

        data = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                barcode_text = self.process_image(file_path)
                if barcode_text:
                    data.append((file_name, barcode_text))
        return data


    
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
