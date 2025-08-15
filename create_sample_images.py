#!/usr/bin/env python3
"""
สร้างไฟล์ JPG ตัวอย่างที่มี QR โค้ดสำหรับทดสอบแอป
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_qr_images():
    """สร้างไฟล์ JPG ตัวอย่างที่มี QR โค้ด"""
    
    # สร้างโฟลเดอร์สำหรับเก็บไฟล์ตัวอย่าง
    sample_dir = "sample_images"
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
    
    # ข้อมูลสำหรับสร้าง QR โค้ด
    sample_data = [
        "PROD001_Apple_iPhone15",
        "BOOK123_Python_Programming",
        "INV2024_Computer_Monitor",
        "DOC456_Important_Document",
        "ID789_Employee_Badge"
    ]
    
    for i, data in enumerate(sample_data, 1):
        # สร้าง QR โค้ด
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # สร้างภาพ QR โค้ด
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # สร้างภาพขนาดใหญ่กว่าเพื่อใส่ QR โค้ด
        canvas = Image.new('RGB', (400, 300), 'white')
        
        # วางจาง QR โค้ดกึ่งกลางภาพ
        qr_resized = qr_img.resize((200, 200))
        canvas.paste(qr_resized, (100, 50))
        
        # เพิ่มข้อความใต้ QR โค้ด
        draw = ImageDraw.Draw(canvas)
        try:
            # ลองใช้ฟอนต์ default
            font = ImageFont.load_default()
        except:
            font = None
        
        text = f"Sample {i}: {data}"
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            text_width = len(text) * 6
            text_height = 10
            
        x = (400 - text_width) // 2
        draw.text((x, 260), text, fill="black", font=font)
        
        # บันทึกเป็นไฟล์ JPG
        filename = f"sample_{i:02d}.jpg"
        filepath = os.path.join(sample_dir, filename)
        canvas.save(filepath, "JPEG", quality=95)
        
        print(f"สร้างไฟล์: {filepath}")
        print(f"  QR โค้ด: {data}")
    
    print(f"\nสร้างไฟล์ตัวอย่างทั้งหมด {len(sample_data)} ไฟล์ในโฟลเดอร์ '{sample_dir}'")
    print(f"เส้นทางโฟลเดอร์: {os.path.abspath(sample_dir)}")
    
    return os.path.abspath(sample_dir)

if __name__ == "__main__":
    sample_path = create_sample_qr_images()
    print(f"\nใช้เส้นทางนี้ในแอป: {sample_path}")