"""
照片分類工具 - Photo Classifier

功能說明：
  使用 face_recognition 庫自動偵測照片中的人臉數量，
  並將照片分類到三個資料夾：
  • solo：個人照（1張人臉）
  • group：合照（2張或以上人臉）
  • scenery：風景照（0張人臉）

工作流程：
  1. 掃描 . 目前資料夾內的所有圖片
  2. 使用 face_recognition 偵測人臉位置和數量
  3. 過濾掉太小的人臉（面積小於圖片的 0.xx%）以避免誤判
  4. 根據人臉數量分類照片，複製到對應的子資料夾
  5. 統計分類結果並顯示報告

"""

import os
import shutil
import cv2
import face_recognition

# ================= 配置路徑 =================
source_dir = r'.'  #照片的來源資料夾路徑
base_target_dir = r'./photo_classified' #分類後照片的目標資料夾路徑

# 設定過濾門檻：人臉面積必須超過整張照片的幾 % (例如 1% = 0.01)
MIN_FACE_SIZE_RATIO = 0.0012  # 稍微提高門檻以過濾遠方路人
DETECTION_MODEL = "hog"      # 偵測模型（"hog" 或 "cnn"，有GPU可用時選 cnn）
# =================


# 定義子資料夾
folders = {
    'solo': os.path.join(base_target_dir, 'solo'),
    'group': os.path.join(base_target_dir, 'group'),
    'scenery': os.path.join(base_target_dir, 'scenery')
}

# 建立資料夾
for path in folders.values():
    os.makedirs(path, exist_ok=True)

def classify_photos():
    print("開始使用 face_recognition 進行辨識...")
    
    # 統計計數
    total_count = 0
    solo_count = 0
    group_count = 0
    scenery_count = 0

    valid_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f)) and f.lower().endswith(valid_extensions)]
    
    for filename in files:
        file_path = os.path.join(source_dir, filename)
        
        # 1. 載入影像檔案
        try:
            image = face_recognition.load_image_file(file_path)
            
            # 取得照片總像素面積
            img_height, img_width, _ = image.shape
            total_area = img_height * img_width

            # 2. 偵測人臉位置
            face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1, model=DETECTION_MODEL)
            
            # 過濾掉太小的人臉 (路人或誤判)
            valid_faces = []
            for (top, right, bottom, left) in face_locations:
                face_area = (bottom - top) * (right - left)
                face_ratio = face_area / total_area
                # --- 新增這行來觀察數值 ---
                #print(f"檔案: {filename}, 人臉比例: {face_ratio:.5f}")

                if face_ratio >= MIN_FACE_SIZE_RATIO:
                    valid_faces.append((top, right, bottom, left))
            
            face_count = len(valid_faces)


            # 3. 分類邏輯
            if face_count == 0:
                target_path = os.path.join(folders['scenery'], filename)
                tag = "[風景]"
                scenery_count += 1
            elif face_count == 1:
                target_path = os.path.join(folders['solo'], filename)
                tag = "[個人]"
                solo_count += 1
            else:
                target_path = os.path.join(folders['group'], filename)
                tag = f"[合照({face_count}人)]"
                group_count += 1

            # 4. 執行複製 (保留原始日期、光圈快門資訊)
            shutil.copy2(file_path, target_path)
            total_count += 1
            print(f"{tag} 處理完畢: {filename}")
            
        except Exception as e:
            print(f"無法處理檔案 {filename}: {e}")

    # 列印統計結果
    print("\n" + "="*50)
    print("照片分類統計")
    print("="*50)
    print(f"> 掃描總數：{total_count} 張")
    print(f"> 個人照 (solo)：{solo_count} 張")
    print(f"> 合照 (group)：{group_count} 張")
    print(f"> 風景照 (scenery)：{scenery_count} 張")
    print("="*50 + "\n")
    print("\n所有照片分類完成！")

if __name__ == "__main__":
    classify_photos()