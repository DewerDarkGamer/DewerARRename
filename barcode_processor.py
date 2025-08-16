import cv2
import numpy as np
from pathlib import Path

# Try to import pyzbar, fall back to OpenCV QR detection if not available
try:
    from pyzbar import pyzbar
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False

class BarcodeProcessor:
    def __init__(self):
        pass

    def read_barcodes(self, image_path):
        """
        อ่านบาร์โค้ดจากไฟล์รูปภาพ
        :param image_path: path ของไฟล์รูปภาพ (เช่น .jpg, .png)
        :return: list ของข้อความที่ถอดได้จากบาร์โค้ด
        """
        # โหลดภาพเป็นสีเทา (grayscale)
        image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        if image is None:
            return []

        results = []
        
        if PYZBAR_AVAILABLE:
            # ใช้ pyzbar ถอดบาร์โค้ด
            barcodes = pyzbar.decode(image)
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                results.append(barcode_data)
        else:
            # ใช้ OpenCV QR code detector เป็น fallback
            qr_detector = cv2.QRCodeDetector()
            data, bbox, _ = qr_detector.detectAndDecode(image)
            if data:
                results.append(data)

        return results
    
    def process_file(self, file_path):
        """
        ประมวลผลไฟล์เดี่ยวเพื่อสกัดข้อมูลบาร์โค้ด
        :param file_path: Path object หรือ string ของไฟล์รูปภาพ
        :return: dict ที่มีผลลัพธ์การประมวลผล
        """
        try:
            file_path = Path(file_path)
            barcodes = self.read_barcodes(file_path)
            
            if barcodes:
                # ใช้บาร์โค้ดตัวแรกที่พบ
                barcode_data = barcodes[0]
                
                # สร้างชื่อไฟล์ใหม่จากข้อมูลบาร์โค้ด
                # ลบอักขระที่ไม่เหมาะสมสำหรับชื่อไฟล์
                safe_barcode = self._make_safe_filename(barcode_data)
                new_name = f"{safe_barcode}.jpg"
                
                return {
                    'success': True,
                    'barcode_data': barcode_data,
                    'barcode_type': 'QR/Barcode',
                    'new_name': new_name,
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'barcode_data': None,
                    'barcode_type': None,
                    'new_name': None,
                    'error': 'No barcode found in image'
                }
                
        except Exception as e:
            return {
                'success': False,
                'barcode_data': None,
                'barcode_type': None,
                'new_name': None,
                'error': str(e)
            }
    
    def _make_safe_filename(self, text):
        """
        แปลงข้อความให้เหมาะสมสำหรับชื่อไฟล์
        :param text: ข้อความต้นฉบับ
        :return: ข้อความที่ปลอดภัยสำหรับชื่อไฟล์
        """
        # อักขระที่ไม่อนุญาตในชื่อไฟล์
        invalid_chars = '<>:"/\\|?*'
        
        # แทนที่อักขระที่ไม่อนุญาตด้วย underscore
        safe_text = text
        for char in invalid_chars:
            safe_text = safe_text.replace(char, '_')
        
        # ลบช่องว่างที่เกินและแทนที่ด้วย underscore
        safe_text = '_'.join(safe_text.split())
        
        # จำกัดความยาวชื่อไฟล์
        if len(safe_text) > 100:
            safe_text = safe_text[:100]
        
        return safe_text
