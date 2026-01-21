# 這段程式碼由 AI (Gemini) 協助生成，用於批次處理照片檔案。
#
# 主要功能：
#   - 讀取使用者提供的每日筆記檔案 (mynote.txt)。
#   - 根據照片的辨識內容和對應日期的筆記，透過 Gemini AI 產生描述性的關鍵字。
#   - 將這些關鍵字附加到檔案名稱中，使檔案更具意義和可搜尋性。
#   - 流程包含：解析筆記、找出需要重新命名的檔案，以及呼叫 AI 來生成新檔名。
#   - API 呼叫為 client.files.upload(上傳檔案) 和client.models.generate_content(生成內容)

import os
from pathlib import Path
import re
import time
from google import genai  #Google Gemini SDK


# --- Configuration ---
# 1. Set your API Key as an environment variable named GOOGLE_API_KEY
# 讀取多組金鑰
ALL_KEYS = [os.getenv('GEMINI_API_KEY_1'), os.getenv('GEMINI_API_KEY_2'), os.getenv('GEMINI_API_KEY_3'), os.getenv('GEMINI_API_KEY_4')]
API_KEYS = [k for k in ALL_KEYS if k]  # 過濾掉沒設定到的空值
print(f"有效的API Key 有 {len(API_KEYS)} 把")

# 2. Define the directory where your photos are located.
PHOTO_DIRECTORY = Path('.') 

# 3. Define the name of your notes file.
NOTES_FILE = 'mynote.txt'

# 4. Gemini model configuration
#MODEL_NAME = "gemini-2.5-pro"  #每日要求數(RPD)=100
MODEL_NAME = "gemini-2.5-flash"  # 每日要求數(RPD)=250

# --- End of Configuration ---


#解析筆記檔案
def parse_notes(file_path):
    """
    尋找所有格式為 月/日 的日期，並將日期後面的文字視為當天的筆記內容。
    Parses the mynote.txt file and returns a dictionary mapping dates to notes.
    """
    notes = {}
    if not file_path.exists():
        print(f"Warning: Notes file '{file_path}' not found.")
        return notes

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find dates (e.g., 9/10, 12/31) and the text that follows
    date_pattern = re.compile(r'(\d{1,2}/\d{1,2})')
    sections = date_pattern.split(content)
    
    # The first element is the text before any date, so we skip it.
    # Then we iterate in pairs: (date, text).
    for i in range(1, len(sections), 2):
        date_key = sections[i]
        note_text = sections[i+1].strip()
        notes[date_key] = note_text
        
    return notes


#篩選未命名檔案
def get_files_to_rename(directory):
    """
    找出尚未被重新命名的圖片檔
    Finds all image files in the directory that have not been renamed yet.
    A file is considered "not renamed" if its name is in the format YYYY-MM-DD_NUM.ext
    """
    unnamed_files = []
    # This regex matches filenames like '2025-09-10_51.jpg' but not '2025-09-10_51_keyword.jpg'
    # It ensures we don't try to rename files that already have descriptive keywords.
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}_\d{1,}\.(jpg|jpeg|png)$', re.IGNORECASE)
    
    for file_path in directory.iterdir():
        if file_path.is_file() and pattern.match(file_path.name):
            unnamed_files.append(file_path)
            
    return sorted(unnamed_files)


# 呼叫 AI 生成新檔名 (上傳圖片和文字筆記到 Gemini API)
def generate_new_filename(client_dict, image_path, notes_for_date):
    """
    Uses the Gemini API to generate a new filename based on the image and notes.
    包含自動切換 API Key 的邏輯。
    """
    original_stem = image_path.stem
    original_suffix = image_path.suffix
    
    prompt = f"""
    You are an expert file renamer. Your task is to analyze the provided image and the context from the text notes for that day.
    Based on this analysis, generate a new, descriptive filename.

    **Instructions:**
    1.  The new filename MUST start with the exact original name: `{original_stem}`.
    2.  Append descriptive keywords based on the image content and notes. Separate keywords with underscores (`_`).
    3.  Do NOT include keywords such as: 人像, 人物, 景觀, 女子, 男子, 女性, 男性, 合照, 多人合照, 比讚, 比YA, 微笑, 笑臉.
    4.  Do NOT change the original file extension (`{original_suffix}`).
    5.  If the notes do not seem to match the image, rely only on the visual content of the image for keywords.
    6.  Your response must be ONLY the new filename and nothing else.
    
    **Example:**
    If the original name is 2025-09-10_052 and the image shows a magnetic paper towel holder from Nitori, 
    a good response would be: 2025-09-10_052_宜得利_磁吸紙巾收納架.jpg
    
    **Context from notes for this day:**
    ---
    {notes_for_date if notes_for_date else "No notes provided for this day."} 
    ---
    """
    
    max_retries = 10

    for i in range(max_retries):
        try:
            # 取得當前正在使用的 client
            client = client_dict['client']
            
            # 上傳檔案
            image_file = client.files.upload(file=str(image_path))

            # 生成內容
            response = client.models.generate_content(
                #這裡需要傳入模型名稱的字串（例如 'gemini-2.5-flash'）
                model = MODEL_NAME,
                contents = [prompt, image_file],
            )
            
            # 成功後刪除遠端檔案
            client.files.delete(name=image_file.name)
            
            new_name = response.text.strip().replace('\n', '')
            if new_name.startswith(original_stem) and new_name.endswith(original_suffix):
                return new_name
            else:
                print(f"  - Warning: AI returned an invalid format: '{new_name}'. Skipping.")
                return None
                
        except Exception as e:
            error_msg = str(e)
            
            # 1. 核心切換邏輯：處理 429 錯誤 (處理單個檔案: 配額超限,切換其他API KEY) ---
            if "429" in error_msg or "Quota exceeded" in error_msg:
                client_dict['key_index'] += 1 # 從 API_KEYS 切換下一組金鑰
                
                if client_dict['key_index'] < len(API_KEYS):
                    new_key = API_KEYS[client_dict['key_index']]
                    print(f"\n⚠️ Key {client_dict['key_index']} 額度已滿，切換至下一把 Key...")
                    # 重新初始化容器內的 client
                    client_dict['client'] = genai.Client(api_key=new_key)
                    # 使用新 Key 重試當前檔案
                    continue 
                else:
                    print("\n❌ 所有 API Key 額度均已耗盡。腳本將強制停止。")
                    raise 

            # 2. 處理 503 錯誤 (服務暫時不可用)
            elif "503" in error_msg and i < max_retries - 1:
                wait_time = 2 ** i
                print(f"  - Received 503 error. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            # 3. 其他錯誤: 達到最大重試次數或遇到其他錯誤時，跳過當前檔案。
            else:
                print(f"  - Error calling Gemini API: {error_msg}. Skipping file.")
                return None

    return None

def main():
    """
    Main function to orchestrate the renaming process.
    """
    # 1. 檢查是否有任何金鑰可用
    if not API_KEYS:
        print("Error: No API keys set.")
        return
    
    print("正在初始化 Gemini Client...")
    
    # 2. 直接使用 API_KEYS 的第一個金鑰初始化容器
    client_dict = {
        'client': genai.Client(api_key=API_KEYS[0]),
        'key_index': 0
    }

    print("Starting photo renaming process...")
    
    notes_path = PHOTO_DIRECTORY / NOTES_FILE
    notes_by_date = parse_notes(notes_path)
    
    files_to_process = get_files_to_rename(PHOTO_DIRECTORY)
    
    if not files_to_process:
        print("No files to rename. All images seem to have descriptive names already.")
        return

    print(f"Found {len(files_to_process)} files to rename.")


    # 新增計數器
    renamed_count = 0
    
    try:
        for file_path in files_to_process:
            print(f"\nProcessing '{file_path.name}'...")
            
            # 提取日期 Extract date from filename (e.g., '2025-09-12' -> '9/12')
            try:
                date_parts = file_path.stem.split('_')[0].split('-')
                month = int(date_parts[1])
                day = int(date_parts[2])
                notes_key = f"{month}/{day}"
            except (IndexError, ValueError):
                print(f"  - Could not parse date from filename. Skipping.")
                continue
                
            #根據提取的 月/日 從筆記字典中找到對應的筆記內容。
            notes_for_date = notes_by_date.get(notes_key, "")
            
            #生成新檔名
            new_filename = generate_new_filename(client_dict, file_path, notes_for_date)

            
            if new_filename:
                try:
                    new_path = file_path.with_name(new_filename)
                    if new_path.exists():
                        print(f"  - Error: A file named '{new_filename}' already exists. Skipping.")
                        continue
                    
                    file_path.rename(new_path)
                    print(f"  - Renamed to: '{new_filename}'")
                    renamed_count += 1  # 成功重命名時增加計數器
                    
                except OSError as e:
                    print(f"  - Error renaming file: {e}")
    
    except Exception as e:
        # 捕捉任何未預期的例外狀況（如 API 額度耗盡）
        error_msg = str(e)
        if "所有 API Key 額度均已耗盡" in error_msg or "Quota exceeded" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print(f"\n⚠️  API 額度已耗盡，停止處理剩餘檔案。")
        else:
            print(f"\n⚠️  發生錯誤，停止處理: {error_msg}")
    
   # 輸出統計結果
    print(f"\n{'='*50}")
    print(f"命名完成！總共處理了 {renamed_count} 張照片。")
    print("\nRenaming process complete.")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
