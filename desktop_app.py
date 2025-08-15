#!/usr/bin/env python3
"""
Desktop Application for JPG Barcode Renamer
Uses tkinter for GUI instead of web-based Streamlit
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.ttk import Progressbar
import os
import threading
from pathlib import Path
import pandas as pd
from barcode_processor import BarcodeProcessor
from PIL import Image, ImageTk

class BarcodeRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JPG Barcode Renamer - Desktop Application")
        self.root.geometry("900x700")
        
        # Variables
        self.folder_path = tk.StringVar()
        self.processed_files = []
        self.preview_data = []
        
        self.setup_gui()
        
    def setup_gui(self):
        """สร้าง GUI elements"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📷 JPG Barcode Renamer", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        subtitle_label = ttk.Label(main_frame, 
                                  text="Application for renaming JPG files using barcode data from images")
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Folder selection section
        folder_frame = ttk.LabelFrame(main_frame, text="1. Select folder containing JPG files", padding="10")
        folder_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(1, weight=1)
        
        ttk.Label(folder_frame, text="Folder path:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(folder_frame, text="Browse Folder", command=self.browse_folder)
        browse_btn.grid(row=0, column=2)
        
        # File info section
        self.info_label = ttk.Label(main_frame, text="", foreground="blue")
        self.info_label.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        # Process section
        process_frame = ttk.LabelFrame(main_frame, text="2. Process files", padding="10")
        process_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.scan_btn = ttk.Button(process_frame, text="🔍 Scan Barcodes", 
                                  command=self.start_scanning, state="disabled")
        self.scan_btn.grid(row=0, column=0, padx=(0, 10))
        
        info_label2 = ttk.Label(process_frame, text="💡 Click button to scan barcodes from all files")
        info_label2.grid(row=0, column=1, sticky=tk.W)
        
        # Progress bar
        self.progress = Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.grid(row=6, column=0, columnspan=3)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="3. Results", padding="10")
        results_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
        # Buttons frame
        buttons_frame = ttk.Frame(results_frame)
        buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.rename_btn = ttk.Button(buttons_frame, text="🔄 Rename Files", 
                                    command=self.start_renaming, state="disabled")
        self.rename_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.reset_btn = ttk.Button(buttons_frame, text="🔄 Reset", 
                                   command=self.reset_app)
        self.reset_btn.grid(row=0, column=1)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.results_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def browse_folder(self):
        """Browse for folder"""
        folder = filedialog.askdirectory(title="Select folder containing JPG files")
        if folder:
            self.folder_path.set(folder)
            self.check_folder()
            
    def check_folder(self):
        """Check folder and JPG files"""
        folder = self.folder_path.get()
        if not folder:
            return
            
        if not os.path.exists(folder):
            self.info_label.config(text="❌ Folder not found", foreground="red")
            self.scan_btn.config(state="disabled")
            return
            
        if not os.path.isdir(folder):
            self.info_label.config(text="❌ Path is not a folder", foreground="red")
            self.scan_btn.config(state="disabled")
            return
            
        # Find JPG files
        jpg_files = []
        for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']:
            jpg_files.extend(Path(folder).glob(ext))
            
        if not jpg_files:
            self.info_label.config(text="⚠️ No JPG files found in folder", foreground="orange")
            self.scan_btn.config(state="disabled")
            return
            
        self.info_label.config(text=f"✅ Found {len(jpg_files)} JPG files", 
                              foreground="green")
        self.scan_btn.config(state="normal")
        self.jpg_files = jpg_files
        
    def start_scanning(self):
        """Start barcode scanning in separate thread"""
        self.scan_btn.config(state="disabled")
        self.rename_btn.config(state="disabled")
        
        # Start scanning thread
        thread = threading.Thread(target=self.scan_barcodes)
        thread.daemon = True
        thread.start()
        
    def scan_barcodes(self):
        """Scan barcodes from all files"""
        processor = BarcodeProcessor()
        self.preview_data = []
        
        total_files = len(self.jpg_files)
        
        for i, file_path in enumerate(self.jpg_files):
            progress = (i + 1) / total_files * 100
            
            # Update progress bar in main thread
            self.root.after(0, self.update_progress, progress, f"Processing: {file_path.name}")
            
            result = processor.process_file(file_path)
            result['original_name'] = file_path.name
            result['file_path'] = str(file_path)
            self.preview_data.append(result)
        
        # Processing complete
        self.root.after(0, self.scanning_complete)
        
    def update_progress(self, value, text):
        """Update progress bar"""
        self.progress['value'] = value
        self.progress_label.config(text=text)
        
    def scanning_complete(self):
        """Scanning complete"""
        self.progress['value'] = 100
        self.progress_label.config(text="✅ Processing complete!")
        
        self.show_preview_results()
        self.scan_btn.config(state="normal")
        
    def show_preview_results(self):
        """Show scanning results"""
        self.results_text.delete(1.0, tk.END)
        
        successful_files = [item for item in self.preview_data if item['success']]
        failed_files = [item for item in self.preview_data if not item['success']]
        
        # Summary
        summary = f"📊 Summary:\n"
        summary += f"  - Total files: {len(self.preview_data)}\n"
        summary += f"  - Successful: {len(successful_files)}\n"
        summary += f"  - Failed: {len(failed_files)}\n\n"
        
        self.results_text.insert(tk.END, summary)
        
        if successful_files:
            self.results_text.insert(tk.END, "✅ Files that can be renamed:\n")
            self.results_text.insert(tk.END, "-" * 80 + "\n")
            
            for item in successful_files:
                line = f"Original name: {item['original_name']}\n"
                line += f"New name: {item['new_name']}\n"
                line += f"Barcode data: {item['barcode_data']}\n"
                line += f"Type: {item['barcode_type']}\n"
                line += "-" * 40 + "\n"
                self.results_text.insert(tk.END, line)
                
            self.rename_btn.config(state="normal")
        
        if failed_files:
            self.results_text.insert(tk.END, "\n❌ Files that cannot be renamed:\n")
            self.results_text.insert(tk.END, "-" * 80 + "\n")
            
            for item in failed_files:
                line = f"Filename: {item['original_name']}\n"
                line += f"Reason: {item['error']}\n"
                line += "-" * 40 + "\n"
                self.results_text.insert(tk.END, line)
                
    def start_renaming(self):
        """Start file renaming process"""
        successful_files = [item for item in self.preview_data if item['success']]
        
        if not successful_files:
            messagebox.showwarning("Warning", "No files can be renamed")
            return
            
        # Confirm renaming
        result = messagebox.askyesno("Confirm", 
                                    f"Do you want to rename {len(successful_files)} files?\n\n" +
                                    "⚠️ File renaming cannot be undone")
        
        if result:
            self.rename_btn.config(state="disabled")
            
            # Start renaming thread
            thread = threading.Thread(target=self.rename_files, args=(successful_files,))
            thread.daemon = True
            thread.start()
            
    def rename_files(self, successful_files):
        """Actually rename files"""
        results = []
        total_files = len(successful_files)
        
        for i, file_info in enumerate(successful_files):
            progress = (i + 1) / total_files * 100
            
            self.root.after(0, self.update_progress, progress, 
                           f"Renaming: {file_info['original_name']}")
            
            try:
                original_path = Path(file_info['file_path'])
                new_path = original_path.parent / file_info['new_name']
                
                # Check if new filename already exists
                if new_path.exists():
                    base_name = new_path.stem
                    extension = new_path.suffix
                    counter = 1
                    while new_path.exists():
                        new_path = original_path.parent / f"{base_name}_{counter}{extension}"
                        counter += 1
                
                original_path.rename(new_path)
                results.append({
                    'original_name': file_info['original_name'],
                    'new_name': new_path.name,
                    'success': True,
                    'error': None
                })
            except Exception as e:
                results.append({
                    'original_name': file_info['original_name'],
                    'new_name': file_info['new_name'],
                    'success': False,
                    'error': str(e)
                })
        
        # Renaming complete
        self.root.after(0, self.renaming_complete, results)
        
    def renaming_complete(self, results):
        """Renaming complete"""
        self.progress['value'] = 100
        self.progress_label.config(text="✅ File renaming complete!")
        
        self.show_rename_results(results)
        self.rename_btn.config(state="disabled")
        
    def show_rename_results(self, results):
        """Show renaming results"""
        self.results_text.delete(1.0, tk.END)
        
        successful_renames = [r for r in results if r['success']]
        failed_renames = [r for r in results if not r['success']]
        
        # Summary
        summary = f"🎉 File renaming results:\n"
        summary += f"  - Total files: {len(results)}\n"
        summary += f"  - Successfully renamed: {len(successful_renames)}\n"
        summary += f"  - Failed to rename: {len(failed_renames)}\n\n"
        
        self.results_text.insert(tk.END, summary)
        
        if successful_renames:
            self.results_text.insert(tk.END, "✅ Successfully renamed files:\n")
            self.results_text.insert(tk.END, "-" * 80 + "\n")
            
            for item in successful_renames:
                line = f"Original name: {item['original_name']}\n"
                line += f"New name: {item['new_name']}\n"
                line += "-" * 40 + "\n"
                self.results_text.insert(tk.END, line)
        
        if failed_renames:
            self.results_text.insert(tk.END, "\n❌ Failed to rename files:\n")
            self.results_text.insert(tk.END, "-" * 80 + "\n")
            
            for item in failed_renames:
                line = f"Filename: {item['original_name']}\n"
                line += f"Reason: {item['error']}\n"
                line += "-" * 40 + "\n"
                self.results_text.insert(tk.END, line)
        
        messagebox.showinfo("Complete", 
                           f"File renaming complete!\n" +
                           f"Successful: {len(successful_renames)} files\n" +
                           f"Failed: {len(failed_renames)} files")
        
    def reset_app(self):
        """Reset application"""
        self.folder_path.set("")
        self.processed_files = []
        self.preview_data = []
        self.info_label.config(text="")
        self.progress['value'] = 0
        self.progress_label.config(text="")
        self.results_text.delete(1.0, tk.END)
        self.scan_btn.config(state="disabled")
        self.rename_btn.config(state="disabled")

def main():
    root = tk.Tk()
    app = BarcodeRenamerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()