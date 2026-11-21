# 批次處理照片檔案-加上日期和流水號
#
# 主要功能：
#   - 根據照片的 EXIF 拍攝時間 (DateTimeOriginal) 重新命名檔案。
#   - 檔案命名格式為 yyyy-mm-dd_NNN.ext，其中 NNN 為三位數流水號。 ext為副檔名，不更動。
#   - 使用 ExifTool 命令行工具進行操作。
#   - 執行前請務必備份原始照片。

import os
import subprocess
import collections
import re
from datetime import datetime

def has_chinese(text):
    """檢查字串裡是否有中文字符"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def get_date_from_filename(filepath):
    filename = os.path.basename(filepath)
    
    # 1. 偵測 13 位數的 Unix 毫秒時間戳記 (例如 1783665903016)
    timestamp_match = re.search(r'(?:\D|^)(\d{13})(?:\D|$)', filename)
    if timestamp_match:
        try:
            ts = int(timestamp_match.group(1)) / 1000.0
            return datetime.fromtimestamp(ts)
        except Exception:
            pass

    # 2. 偵測 8 位數日期格式 YYYYMMDD (例如 20260710)
    date8_match = re.search(r'(?:\D|^)((?:20\d{2})(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01]))(?:\D|$)', filename)
    if date8_match:
        try:
            return datetime.strptime(date8_match.group(1), '%Y%m%d')
        except Exception:
            pass

    # 3. 偵測帶底線或橫線的 YYYY-MM-DD 格式
    date_sep_match = re.search(r'(?:\D|^)((?:20\d{2})[-_](?:0[1-9]|1[0-2])[-_](?:0[1-9]|[12]\d|3[01]))(?:\D|$)', filename)
    if date_sep_match:
        try:
            date_str = date_sep_match.group(1).replace('_', '-')
            return datetime.strptime(date_str, '%Y-%m-%d')
        except Exception:
            pass

    return None


def get_exif_date(filepath):
    try:
        cmd = ["exiftool", "-s3", "-DateTimeOriginal", filepath]
        # 拿掉 text=True，讓 stdout 是 bytes
        result = subprocess.run(cmd, capture_output=True, check=True)
        
        # 用 utf-8 解碼，遇到錯就用 ? 取代
        date_str = result.stdout.decode('utf-8', errors='replace').strip()
        
        if date_str:
            return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S'), True
        else:
            # EXIF 沒找到，嘗試從檔名解析
            filename_date = get_date_from_filename(filepath)
            if filename_date:
                print(f"檔案 {filepath}: 未找到 EXIF 拍攝時間，但從檔名解析出日期：{filename_date.strftime('%Y-%m-%d')}。")
                return filename_date, True
            else:
                print(f"檔案 {filepath}: 未找到 EXIF 拍攝時間且檔名無日期資訊。")
                try:
                    return datetime.fromtimestamp(os.path.getmtime(filepath)), False
                except OSError:
                    return None, False
            
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as e:
        print(f"無法處理檔案 {filepath}: {e}。將嘗試使用檔名解析或檔案修改時間。")
        filename_date = get_date_from_filename(filepath)
        if filename_date:
            return filename_date, True
        try:
            return datetime.fromtimestamp(os.path.getmtime(filepath)), False
        except OSError as oe:
            print(f"無法獲取檔案 {filepath} 的修改時間: {oe}")
            return None, False


def rename_photos_by_date():
    """根據拍攝日期重新命名目前目錄中的照片"""
    
    # 支援的圖片副檔名
    supported_extensions = ('.jpg', '.jpeg', '.png')
    
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}_\d{3}(?:_.+)?\.(jpg|jpeg|png|JPG|JPEG|PNG)$', re.IGNORECASE)


    # 收集檔案列表
    #files_to_process = [f for f in os.listdir('.') if f.lower().endswith(supported_extensions)]
    # 收集檔案列表 過濾掉有中文關鍵字的檔名
    files_to_process = []
    for f in os.listdir('.'):
        if not f.lower().endswith(supported_extensions):
            continue
        if has_chinese(f):
            print(f"跳過有中文關鍵字的檔案：{f}")
            continue
        # 如果檔名已經是 yyyy-mm-dd_NNN 或 yyyy-mm-dd_NNN_xxx 格式→ 直接跳過
        if date_pattern.match(f):
            #print(f"檔案 '{f}' 已含日期與編號，保留既有關鍵字，跳過。")
            print(f"跳過有日期與編號的檔案：{f}")
            continue
        files_to_process.append(f)

    if not files_to_process:
        print("在目前目錄中找不到任何支援的圖片檔案。")
        return

    # 收集並解析所有檔案的日期資訊
    parsed_files = []
    has_date_info_dates = []
    
    for filename in files_to_process:
        res = get_exif_date(filename)
        if res:
            dt, has_date_info = res
            if dt:
                parsed_files.append({
                    'filename': filename,
                    'datetime': dt,
                    'has_date_info': has_date_info
                })
                if has_date_info:
                    has_date_info_dates.append(dt)

    if not parsed_files:
        print("在目前目錄中找不到任何可處理的圖片檔案。")
        return

    # 找出其他批次檔名中最新的日期 (latest date among files with date info)
    latest_valid_date = None
    if has_date_info_dates:
        latest_valid_date = max(has_date_info_dates)
        print(f"\n批次中包含日期資訊的最晚日期為：{latest_valid_date.strftime('%Y-%m-%d')}")
    else:
        print("\n批次中沒有任何檔案包含日期資訊。將使用各個檔案的修改時間。")

    # 按日期對檔案進行分組
    photos_by_date = collections.defaultdict(list)
    for item in parsed_files:
        filename = item['filename']
        dt = item['datetime']
        has_date_info = item['has_date_info']
        
        if not has_date_info and latest_valid_date:
            # 無日期特徵的檔名，使用批次中最新的日期
            target_date = latest_valid_date
            # 將其排序時間設為最新日期的日期加上原修改時間的時間部分，以保留原本的排序順序
            dt_combined = datetime.combine(target_date.date(), dt.time())
            date_key = target_date.strftime('%Y-%m-%d')
            photos_by_date[date_key].append((dt_combined, filename))
            print(f"檔案 {filename}: 無日期特徵，將套用批次最晚日期：{date_key}")
        else:
            date_key = dt.strftime('%Y-%m-%d')
            photos_by_date[date_key].append((dt, filename))

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

            # 新增：檢查目標檔名是否已存在，避免 [WinError 183] 錯誤
            if os.path.exists(new_filename):
                print(f"跳過 '{old_filename}'，目標檔名'{new_filename}'已存在，以避免覆蓋 。")
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
        print("\n=== 照片重新命名完成 ===")
