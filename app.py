import streamlit as st
import os
import pandas as pd
from pathlib import Path
from barcode_processor import BarcodeProcessor
import time

def main():
    st.set_page_config(
        page_title="JPG Barcode Renamer",
        page_icon="📷",
        layout="wide"
    )
    
    st.title("📷 JPG Barcode Renamer")
    st.markdown("แอปพลิเคชันสำหรับเปลี่ยนชื่อไฟล์ JPG โดยใช้ข้อมูลบาร์โค้ดในรูปภาพ")
    
    # Initialize session state
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = None
    if 'preview_data' not in st.session_state:
        st.session_state.preview_data = None
    if 'selected_folder' not in st.session_state:
        st.session_state.selected_folder = ""
    
    # Folder selection
    st.header("1. เลือกโฟลเดอร์ที่มีไฟล์ JPG")
    folder_path = st.text_input(
        "กรอกเส้นทางโฟลเดอร์:",
        value=st.session_state.selected_folder,
        placeholder="เช่น /path/to/your/jpg/files หรือ C:\\path\\to\\your\\jpg\\files",
        help="กรอกเส้นทางโฟลเดอร์ที่มีไฟล์ JPG ที่ต้องการเปลี่ยนชื่อ"
    )
    
    if folder_path and folder_path != st.session_state.selected_folder:
        st.session_state.selected_folder = folder_path
        st.session_state.processed_files = None
        st.session_state.preview_data = None
    
    if folder_path:
        if not os.path.exists(folder_path):
            st.error(f"❌ ไม่พบโฟลเดอร์: {folder_path}")
            st.info("💡 กรุณาตรวจสอบเส้นทางให้ถูกต้อง")
            return
        
        if not os.path.isdir(folder_path):
            st.error(f"❌ เส้นทางที่ระบุไม่ใช่โฟลเดอร์: {folder_path}")
            return
        
        # Find JPG files
        jpg_files = []
        for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']:
            jpg_files.extend(Path(folder_path).glob(ext))
        
        if not jpg_files:
            st.warning(f"⚠️ ไม่พบไฟล์ JPG ในโฟลเดอร์: {folder_path}")
            return
        
        st.success(f"✅ พบไฟล์ JPG จำนวน {len(jpg_files)} ไฟล์")
        
        # Process files button
        st.header("2. ประมวลผลไฟล์")
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("🔍 สแกนบาร์โค้ด", type="primary"):
                process_files(jpg_files)
        
        with col2:
            st.info("💡 กดปุ่มเพื่อสแกนบาร์โค้ดจากไฟล์ทั้งหมด")
        
        # Show preview if available
        if st.session_state.preview_data is not None:
            show_preview()
        
        # Show results if available
        if st.session_state.processed_files is not None:
            show_results()

def process_files(jpg_files):
    """Process JPG files to extract barcode data"""
    processor = BarcodeProcessor()
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    preview_data = []
    total_files = len(jpg_files)
    
    for i, file_path in enumerate(jpg_files):
        progress = (i + 1) / total_files
        progress_bar.progress(progress)
        status_text.text(f"กำลังประมวลผล: {file_path.name} ({i + 1}/{total_files})")
        
        result = processor.process_file(file_path)
        result['original_name'] = file_path.name
        result['file_path'] = str(file_path)
        preview_data.append(result)
    
    status_text.text("✅ ประมวลผลเสร็จสิ้น!")
    progress_bar.empty()
    status_text.empty()
    
    st.session_state.preview_data = preview_data

def show_preview():
    """Show preview of rename operations"""
    st.header("3. ตัวอย่างการเปลี่ยนชื่อไฟล์")
    
    preview_data = st.session_state.preview_data
    successful_files = [item for item in preview_data if item['success']]
    failed_files = [item for item in preview_data if not item['success']]
    
    # Summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 ไฟล์ทั้งหมด", len(preview_data))
    with col2:
        st.metric("✅ สำเร็จ", len(successful_files))
    with col3:
        st.metric("❌ ล้มเหลว", len(failed_files))
    
    if successful_files:
        st.subheader("✅ ไฟล์ที่สามารถเปลี่ยนชื่อได้")
        
        # Create DataFrame for successful files
        success_df = pd.DataFrame([
            {
                'ชื่อเดิม': item['original_name'],
                'ชื่อใหม่': item['new_name'],
                'ข้อมูลบาร์โค้ด': item['barcode_data'],
                'ประเภทบาร์โค้ด': item['barcode_type']
            }
            for item in successful_files
        ])
        
        st.dataframe(success_df, use_container_width=True)
        
        # Rename button
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔄 เปลี่ยนชื่อไฟล์", type="primary"):
                rename_files(successful_files)
        with col2:
            st.warning("⚠️ การเปลี่ยนชื่อไฟล์ไม่สามารถย้อนกลับได้")
    
    if failed_files:
        st.subheader("❌ ไฟล์ที่ไม่สามารถเปลี่ยนชื่อได้")
        
        # Create DataFrame for failed files
        fail_df = pd.DataFrame([
            {
                'ชื่อไฟล์': item['original_name'],
                'สาเหตุ': item['error']
            }
            for item in failed_files
        ])
        
        st.dataframe(fail_df, use_container_width=True)

def rename_files(successful_files):
    """Actually rename the files"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    total_files = len(successful_files)
    
    for i, file_info in enumerate(successful_files):
        progress = (i + 1) / total_files
        progress_bar.progress(progress)
        status_text.text(f"กำลังเปลี่ยนชื่อ: {file_info['original_name']} → {file_info['new_name']}")
        
        try:
            original_path = Path(file_info['file_path'])
            new_path = original_path.parent / file_info['new_name']
            
            # Check if new filename already exists
            if new_path.exists():
                # Add number suffix to avoid conflicts
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
    
    progress_bar.empty()
    status_text.empty()
    
    st.session_state.processed_files = results
    st.session_state.preview_data = None

def show_results():
    """Show final results of rename operations"""
    st.header("4. ผลลัพธ์การเปลี่ยนชื่อไฟล์")
    
    results = st.session_state.processed_files
    successful_renames = [r for r in results if r['success']]
    failed_renames = [r for r in results if not r['success']]
    
    # Summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 ไฟล์ทั้งหมด", len(results))
    with col2:
        st.metric("✅ เปลี่ยนชื่อสำเร็จ", len(successful_renames))
    with col3:
        st.metric("❌ เปลี่ยนชื่อล้มเหลว", len(failed_renames))
    
    if successful_renames:
        st.subheader("✅ ไฟล์ที่เปลี่ยนชื่อสำเร็จ")
        success_df = pd.DataFrame([
            {
                'ชื่อเดิม': item['original_name'],
                'ชื่อใหม่': item['new_name']
            }
            for item in successful_renames
        ])
        st.dataframe(success_df, use_container_width=True)
    
    if failed_renames:
        st.subheader("❌ ไฟล์ที่เปลี่ยนชื่อล้มเหลว")
        fail_df = pd.DataFrame([
            {
                'ชื่อไฟล์': item['original_name'],
                'สาเหตุ': item['error']
            }
            for item in failed_renames
        ])
        st.dataframe(fail_df, use_container_width=True)
    
    # Reset button
    if st.button("🔄 เริ่มต้นใหม่"):
        st.session_state.processed_files = None
        st.session_state.preview_data = None
        st.rerun()

if __name__ == "__main__":
    main()
