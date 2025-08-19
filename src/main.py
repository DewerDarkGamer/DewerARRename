import cv2
import os
from pyzxing import BarCodeReader
from tkinter import Tk, filedialog

def process_image(image_path):
    reader = BarCodeReader()
    results = reader.decode(image_path)
    if results:
        for r in results:
            print(f"[BARCODE] {r['raw']}")
            return r['raw']
    else:
        print("[INFO] No barcode found")
        return None

def main():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
    )

    if not file_path:
        print("[INFO] No file selected")
        return

    barcode_data = process_image(file_path)
    if barcode_data:
        dir_name, filename = os.path.split(file_path)
        new_name = os.path.join(dir_name, f"{barcode_data}.jpg")
        os.rename(file_path, new_name)
        print(f"[SUCCESS] Renamed file to {new_name}")

if __name__ == "__main__":
    main()
