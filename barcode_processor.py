import cv2
import numpy as np
from pyzbar import pyzbar

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
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            return []

        # ใช้ pyzbar ถอดบาร์โค้ด
        barcodes = pyzbar.decode(image)

        results = []
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            results.append(barcode_data)

        return results
