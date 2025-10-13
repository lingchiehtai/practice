# 這段程式碼由 AI (Gemini) 協助生成，用於批次處理照片檔案。
#
# 主要功能：
#   - 流程包含：找出所有圖片檔案，呼叫 AI 產生關鍵字，並重新命名檔案。
#   ###忽略照片的原始檔名格式。
#   - 根據每張照片的內容，透過 Gemini AI 產生描述性的關鍵字。
#   - 將這些 AI 生成的關鍵字附加到原始檔案名稱。
#   - 多個關鍵字之間使用底線 "_" 隔開。
#

import os
import re
import time
import google.generativeai as genai
from pathlib import Path

# --- Configuration ---
# 1. Set your API Key as an environment variable named GOOGLE_API_KEY
#    For example, in your terminal: export GOOGLE_API_KEY="YOUR_API_KEY"
API_KEY = os.getenv('GOOGLE_API_KEY')

# 2. Define the directory where your photos are located.
PHOTO_DIRECTORY = Path('.')

# 3. Gemini model configuration
#MODEL_NAME = "gemini-1.5-pro"
MODEL_NAME = "gemini-2.5-flash" # 使用 Flash 模型速度更快，成本更低

GENERATION_CONFIG = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
# --- End of Configuration ---


def get_all_image_files(directory):
    """
    找出資料夾中所有的圖片檔案 (jpg, jpeg, png)。
    """
    image_files = []
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ('.jpg', '.jpeg', '.png'):
            image_files.append(file_path)
    return sorted(image_files)


def generate_keywords_from_image(model, image_path):
    """
    使用 Gemini API 根據圖片內容生成描述性關鍵字。
    包含 API 錯誤的重試邏輯。
    """
    prompt = """
    你是一位專業的圖片內容描述專家。你的任務是分析提供的圖片。
    根據圖片內容，生成一些具描述性的關鍵字。

    **說明：**
    1. 生成的關鍵字必須是簡潔、明確的中文詞彙。
    2. 如果有多個關鍵字，請使用底線 (`_`) 分隔它們。
    3. 你的回應必須**只包含關鍵字字串**，不要有任何額外的文字說明。

    **範例：**
    如果圖片顯示的是一隻在公園裡奔跑的金毛獵犬，一個好的回應會是：
    `金毛獵犬_公園_奔跑`

    如果圖片顯示的是一盤美味的壽司，一個好的回應會是：
    `壽司_日式料理_美食`

    現在，請為這張圖片生成關鍵字。
    """
    
    # 上傳圖片到 Gemini
    image_file = genai.upload_file(path=str(image_path))
    
    max_retries = 5  # 減少重試次數，加快測試
    for i in range(max_retries):
        try:
            response = model.generate_content([prompt, image_file])
            # 清理回應，確保只返回關鍵字字串
            keywords = response.text.strip().replace('\n', '')
            # 移除不必要的符號，例如標點符號或額外的底線
            keywords = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fa5]', '', keywords) # 只保留中文、英文、數字和底線
            
            if keywords:
                return keywords
            else:
                print(f"  - 警告：AI 返回了空的關鍵字。跳過。")
                return None
        except Exception as e:
            print(f"  - 呼叫 Gemini API 發生錯誤：{e}")
            if "503" in str(e) and i < max_retries - 1:
                wait_time = 2 ** i
                print(f"  - 收到 503 錯誤。{wait_time} 秒後重試...")
                time.sleep(wait_time)
            else:
                print("  - 已達最大重試次數或不可重試的錯誤。跳過檔案。")
                return None
    return None


def main():
    """
    主函式，協調整個重新命名的流程。
    """
    if not API_KEY:
        print("錯誤：GOOGLE_API_KEY 環境變數未設定。")
        print("請設定您的 API 金鑰並重新執行腳本。")
        return

    if not PHOTO_DIRECTORY.exists():
        print(f"錯誤：找不到指定的資料夾 '{PHOTO_DIRECTORY}'。")
        print("請檢查 PHOTO_DIRECTORY 變數的路徑設定。")
        return

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        MODEL_NAME,
        safety_settings=SAFETY_SETTINGS,
        generation_config=GENERATION_CONFIG,
    )

    print("開始照片重新命名程序 (基於圖片內容生成關鍵字)...")
    
    files_to_process = get_all_image_files(PHOTO_DIRECTORY)
    
    if not files_to_process:
        print("沒有找到需要處理的圖片檔案 (jpg, jpeg, png)。")
        return

    print(f"找到 {len(files_to_process)} 個檔案需要重新命名。")

    for file_path in files_to_process:
        print(f"\n正在處理 '{file_path.name}'...")
        
        keywords = generate_keywords_from_image(model, file_path)
        
        if keywords:
            try:
                original_stem = file_path.stem
                original_suffix = file_path.suffix
                
                # 組合新的檔名：原始檔名_關鍵字.副檔名
                new_filename = f"{original_stem}_{keywords}{original_suffix}"
                new_path = file_path.with_name(new_filename)
                
                if new_path.exists():
                    print(f"  - 錯誤：檔案 '{new_filename}' 已存在。跳過。")
                    continue
                    
                file_path.rename(new_path)
                print(f"  - 重新命名為: '{new_filename}'")
            except OSError as e:
                print(f"  - 重新命名檔案時發生錯誤：{e}")
        else:
            print(f"  - 無法為 '{file_path.name}' 生成關鍵字。跳過。")

    print("\n重新命名程序完成。")

if __name__ == "__main__":
    main()