# 猜拳手勢辨識 (Rock-Paper-Scissors Image Classification)

## 簡介
本專案使用 TensorFlow/Keras 框架建立一個卷積神經網路 (CNN) 模型，旨在自動辨識手勢圖片中的「剪刀」、「石頭」與「布」。專案涵蓋了從原始資料處理、模型訓練、效能評估到最終推理預測的完整深度學習流程。

## 專案內容
- **資料預處理 (`img_classification.py`)**：包含讀取資料夾結構、資料集視覺化、以及將資料分割為訓練集與測試集的功能。
- **模型架構**：構建多層 CNN 結構，並加入 Dropout 層防止過擬合。
- **結果記錄**：
  - `best_model.keras`：訓練過程中驗證集準確率最高的模型權重。
  - `accuracy_loss_history.csv`：紀錄每一輪 (Epoch) 的訓練與驗證數據。
  - `Accuracy.png` & `Loss.png`：訓練過程的可視化趨勢圖。
- **預測功能**：載入儲存的模型，對 `test-paper` 等目錄下的新圖片進行批次預測與分類統計。

## 重點分析
1. **卷積神經網路 (CNN) 設計**：
   - 使用了 4 層 `Conv2D` 與 `MaxPooling2D` 的組合，濾波器數量從 64 漸進增加至 256，能有效提取由簡入繁的圖像特徵。
   - 使用 `Dense(1024)` 的全連接層配合 `Dropout(0.2)`，平衡了模型的學習能力與泛化能力。
2. **自動化模型管理**：
   - 透過 `ModelCheckpoint` 回調函數監控 `val_accuracy`，確保最終儲存的是表現最佳的模型而非最後一輪的模型。
3. **數據處理優化**：
   - 使用 `ImageDataGenerator` 進行像素歸一化 (Rescale 1/255)，提升模型收斂效率。
   - 提供資料視覺化區塊，在訓練前確認標籤與圖片的正確性。

## 如何執行

### 1. 環境準備
確保您的開發環境已安裝以下必要套件：
```bash
pip install tensorflow pandas matplotlib numpy
```

### 2. 資料集配置
將 Rock-Paper-Scissors 資料集解壓縮並放置於專案根目錄下的 `./rps-cv-images/` 資料夾，結構如下：
- `rps-cv-images/paper/`
- `rps-cv-images/rock/`
- `rps-cv-images/scissors/`

### 3. 執行訓練
執行主程式開始訓練流程。程式會先顯示資料預覽圖，關閉視圖後即開始訓練：
```bash
python img_classification.py
```
*注意：若為首次執行且尚未分割資料，請確保程式中 `split_data` 相關程式碼區塊已取消註解以建立 `./tmp/` 目錄。*

### 4. 檢視結果與預測
- 訓練完成後，檢查產生的 `Accuracy.png` 確保模型無嚴重的過擬合現象。
- 預測結果將直接顯示在終端機中，顯示測試資料夾內每種手勢的預測成功率。

---
*Created by Linda Tai*