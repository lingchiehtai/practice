# 城市自行車租借需求預測 (Seoul Bike Sharing Demand Prediction)

這是一個基於深度學習的迴歸分析專案，旨在使用 TensorFlow/Keras 建立深度神經網路 (DNN) 模型，預測首爾市在不同時間與氣象條件下的自行車租借數量。

## 專案內容

本專案包含以下主要步驟：
1. **資料獲取**：透過 `ucimlrepo` 套件自動下載 UCI Machine Learning Repository 中的首爾自行車租借資料集。
2. **資料清理與處理**：
   - 移除不適用的特徵欄位（如日期、季節等標籤欄位）。
   - 篩選有效的租借紀錄（排除租借數為 0 的資料）。
   - 將資料分割為訓練集 (85%) 與測試集 (15%)。
3. **模型構建**：建立一個包含多層 Dense 層的深度神經網路，並加入資料正規化層 (Normalization)。
4. **訓練與評估**：使用 Adam 優化器與平均絕對誤差 (MAE) 作為損失函數進行訓練。
5. **可視化分析**：繪製訓練損失曲線、預測值與實際值的散佈圖，以及誤差分佈圖。

## 重點分析

*   **特徵工程**：專案選取了與租借量高度相關的特徵，包括 `Hour` (小時)、`Temperature` (溫度)、`Humidity` (濕度)、`Wind speed` (風速) 與 `Visibility` (能見度)。
*   **資料正規化**：由於不同氣象參數的數值範圍差異極大，模型中加入了 `tf.keras.layers.Normalization` 層，這對於加速 DNN 收斂與提升準確度至關重要。
*   **模型架構**：採用了逐漸擴張的神經元設計（32 -> 64 -> 128 -> 256），賦予模型捕捉非線性關係的能力。
*   **效能評估**：
    - **損失函數曲線**：觀察 `train_loss` 與 `val_loss` 是否同步下降，以判斷模型是否過擬合 (Overfitting)。
    - **預測散佈圖**：直觀判斷預測值與 1:1 實際值線的偏離程度。
    - **誤差分佈**：透過直方圖分析預測誤差的集中趨勢。

## 如何執行

### 1. 環境準備
請確保您的 Python 環境中已安裝必要的套件：

```bash
pip install tensorflow matplotlib numpy seaborn ucimlrepo
```

### 2. 執行腳本
在終端機或 IDE 中執行 `regression-rent-bike.py`：

```bash
python regression-rent-bike.py
```

### 3. 查看結果
執行完成後，系統會生成以下檔案：
*   `plot_bike_rental_loss.png`: 訓練過程的損失變化圖。
*   `plot_bike_rental_predict.png`: 預測值與實際值的比對散佈圖。
*   `plot_bike_rental_hist_error.png`: 預測誤差的分佈圖。
*   `dnn_model_rent_bike.keras`: 訓練完成的模型權重檔案。

---
**資料來源**: UCI Machine Learning Repository - Seoul Bike Sharing Demand
**作者**: Linda Tai