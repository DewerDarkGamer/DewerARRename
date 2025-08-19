import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pyzxing import BarCodeReader

def process_file(file_path):
    reader = BarCodeReader(jar_path="libs/zxing/javase-3.5.0.jar")
    results = reader.decode(file_path)
    if results:
        return results[0]['parsed']
    return None

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        result = process_file(file_path)
        if result:
            messagebox.showinfo("Result", f"Barcode: {result}")
        else:
            messagebox.showwarning("Not Found", "No barcode detected")

def open_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        results = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                result = process_file(os.path.join(folder_path, filename))
                if result:
                    results.append(f"{filename} → {result}")
        if results:
            messagebox.showinfo("Results", "\n".join(results))
        else:
            messagebox.showwarning("Not Found", "No barcodes detected in folder")

root = tk.Tk()
root.title("Barcode Reader")

btn_file = tk.Button(root, text="เลือกไฟล์", command=open_file, width=20)
btn_file.pack(pady=10)

btn_folder = tk.Button(root, text="เลือกโฟลเดอร์", command=open_folder, width=20)
btn_folder.pack(pady=10)

root.mainloop()
