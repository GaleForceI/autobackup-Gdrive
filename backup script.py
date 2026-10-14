import os
import shutil
import subprocess
from datetime import datetime

# --- CẤU HÌNH ---
SOURCE_DIR = os.path.expanduser("~/Documents/my_data") # Thư mục bạn muốn backup
BACKUP_NAME_PREFIX = "backup"
REMOTE_TARGET = "gdrive:LinuxBackups" # Tên remote Rclone và thư mục trên Google Drive

def create_zip_backup():
    if not os.path.exists(SOURCE_DIR):
        print(f"[-] Thư mục nguồn {SOURCE_DIR} không tồn tại!")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"/tmp/{BACKUP_NAME_PREFIX}_{timestamp}.zip"
    
    print(f"[*] Đang nén thư mục {SOURCE_DIR}...")
    # Nén thư mục thành định dạng zip
    shutil.make_archive(output_filename.replace('.zip', ''), 'zip', SOURCE_DIR)
    print(f"[+] Đã nén xong: {output_filename}")
    return output_filename

def upload_to_gdrive(file_path):
    print(f"[*] Đang tải tệp lên Google Drive ({REMOTE_TARGET})...")
    # Sử dụng lệnh rclone copy ngầm trong Python
    try:
        result = subprocess.run(
            ["rclone", "copy", file_path, REMOTE_TARGET],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("[+] Tải lên Google Drive thành công!")
    except subprocess.CalledProcessError as e:
        print(f"[-] Lỗi khi tải lên: {e.stderr}")

def main():
    print("=== BẮT ĐẦU QUÁ TRÌNH BACKUP ===")
    zip_file = create_zip_backup()
    if zip_file:
        upload_to_gdrive(zip_file)
        # Dọn dẹp tệp zip tạm sau khi upload xong
        os.remove(zip_file)
        print("[*] Đã dọn dẹp tệp tạm trên hệ thống.")
    print("=== HOÀN TẤT ===")

if __name__ == "__main__":
    main()