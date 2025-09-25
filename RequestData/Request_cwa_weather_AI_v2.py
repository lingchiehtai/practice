#下載cwa網頁中的 颱風警報路徑圖，並依據圖片裡的發布時間來修改檔名

import os
import re
import requests
import google.generativeai as genai
from PIL import Image
from io import BytesIO

MODEL_NAME = "gemini-2.5-flash" 

import os
import re
import requests
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# --- 1. 設定圖片來源 URL ---
pic_url = "https://www.cwa.gov.tw/Data/typhoon/TY_WARN/B20.png"

# --- 2. 配置 Gemini API 金鑰 ---
# 建議從環境變數讀取，更安全
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    print("成功讀取 GOOGLE_API_KEY 環境變數。")
except KeyError:
    print("錯誤：未找到 GOOGLE_API_KEY 環境變數。")
    # 如果您選擇直接寫入金鑰，請取消下面這行的註解並替換為您的金鑰
    # genai.configure(api_key="在此輸入您的API金鑰")
    exit() # 如果沒有API金鑰，程式終止

# --- 3. 創建 Gemini Vision Pro 模型實例 ---
model = genai.GenerativeModel(MODEL_NAME)

def download_and_process_image(url):
    """
    從網路下載圖片，分析內容，然後決定檔名並儲存。
    """
    # 從 URL 中提取原始檔名作為備用
    original_filename_from_url = url.split('/')[-1]
    if not original_filename_from_url: # 如果 URL 以 / 結尾
        original_filename_from_url = "downloaded_image.png"

    print(f"正在從 URL 下載圖片: {url}")
    try:
        # 下載圖片內容
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 如果請求失敗，則會引發錯誤
        
        # 將圖片內容讀入記憶體
        image_bytes = response.content
        img = Image.open(BytesIO(image_bytes))

        # --- 使用 Gemini API 提取資訊 ---
        prompt = (
            "請簡潔地回傳這張圖片中的主要文字。如果看到颱風警報發布時間，請回傳包含'民國'的完整句子。"
            "如果看到'陸續更新中'，請回傳那句話。"
        )
        print("正在使用 Gemini API 分析圖片...")
        api_response = model.generate_content([prompt, img], request_options={"timeout": 60})
        
        if not api_response.text:
            print("警告：Gemini API 未能從圖片中提取到任何文本資訊。")
            final_filename = original_filename_from_url
        else:
            info_text = api_response.text.strip().lower() # 轉換為小寫以便比對
            print(f"從圖片中提取的資訊: '{info_text}'")

            # --- 判斷圖片內容 ---
            if "陸續更新中" in info_text or "updated soon" in info_text:
                print("偵測到圖片內容為更新中訊息。")
                final_filename = original_filename_from_url
            else:
                # --- 嘗試解析資訊並產生新檔名 ---
                match = re.search(
                    r'民國\s*(\d+)\s*年\s*(\d+)\s*月\s*(\d+)\s*日\s*(\d+)\s*時\s*(\d+)\s*分',
                    info_text
                )
                if match:
                    roc_year, month, day, hour, minute = map(str, match.groups())
                    gregorian_year = int(roc_year) + 1911
                    final_filename = (
                        f"pic_颱風警報_"
                        f"{gregorian_year}{month.zfill(2)}{day.zfill(2)}_"
                        f"{hour.zfill(2)}{minute.zfill(2)}.png"
                    )
                    print(f"成功解析日期，新檔名為: {final_filename}")
                else:
                    print("警告：圖片內容非更新中訊息，但也無法解析出日期。")
                    final_filename = original_filename_from_url

        # --- 儲存圖片 ---
        try:
            with open(final_filename, 'wb') as f:
                f.write(image_bytes)
            print("-" * 30)
            print(f"成功！圖片已儲存為: {final_filename}")
            print("-" * 30)
        except IOError as e:
            print(f"儲存檔案 '{final_filename}' 時發生錯誤: {e}")

    except requests.exceptions.RequestException as e:
        print(f"下載圖片時發生網路錯誤: {e}")
    except Exception as e:
        print(f"處理圖片時發生未知錯誤: {e}")


# --- 主程式執行區塊 ---
if __name__ == "__main__":
    download_and_process_image(pic_url)