# 這段程式碼由 AI (Gemini) 協助生成，用於批次處理照片檔案。
#
# 主要功能：
#   - 根據照片的 EXIF 拍攝時間 (DateTimeOriginal) 重新命名檔案。
#   - 檔案命名格式為 yyyy-mm-dd_NNN.ext，其中 NNN 為三位數流水號。 ext為副檔名，不更動。
#   - 使用 ExifTool 命令行工具進行操作。
#   - 執行前請務必備份原始照片。

import os
import subprocess
import collections
from datetime import datetime

def get_exif_date(filepath):
    """使用 ExifTool 獲取照片的拍攝日期"""
    try:
        # -s3 選項讓 ExifTool 只返回標籤的值，不含標籤名稱
        cmd = ["exiftool", "-s3", "-DateTimeOriginal", filepath]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        date_str = result.stdout.strip()
        # 解析時間戳以應對不同格式，並確保排序正確
        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as e:
        print(f"無法處理檔案 {filepath}: {e}")
        return None

def rename_photos_by_date():
    """根據拍攝日期重新命名目前目錄中的照片"""
    # 支援的圖片副檔名
    supported_extensions = ('.jpg', '.jpeg', '.png')
    files_to_process = [f for f in os.listdir('.') if f.lower().endswith(supported_extensions)]

    if not files_to_process:
        print("在目前目錄中找不到任何支援的圖片檔案。")
        return

    # 按日期對檔案進行分組
    photos_by_date = collections.defaultdict(list)
    for filename in files_to_process:
        exif_datetime = get_exif_date(filename)
        if exif_datetime:
            date_key = exif_datetime.strftime('%Y-%m-%d')
            photos_by_date[date_key].append((exif_datetime, filename))

    # 對每個日期的照片進行排序和重新命名
    for date_str, files in photos_by_date.items():
        # 根據完整的拍攝時間排序，確保編號順序正確
        files.sort()
        
        for index, (exif_dt, old_filename) in enumerate(files, 1):
            _, extension = os.path.splitext(old_filename)
            new_filename = f"{date_str}_{index:03d}{extension}"
            
            if old_filename == new_filename:
                print(f"檔案 '{old_filename}' 已是正確格式，跳過。")
                continue

            try:
                print(f"正在將 '{old_filename}' 重新命名為 '{new_filename}'...")
                os.rename(old_filename, new_filename)
            except OSError as e:
                print(f"重新命名 '{old_filename}' 時發生錯誤: {e}")

if __name__ == "__main__":
    # 檢查 exiftool 是否存在
    try:
        subprocess.run(["exiftool", "-ver"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("錯誤：找不到 ExifTool。請確保它已安裝並在系統 PATH 中。" )
    else:
        rename_photos_by_date()
        print("\n照片重新命名完成。")
