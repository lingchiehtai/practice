

# Iris Prediction API

- 這是一個使用 FastAPI 建立的簡單機器學習模型預測 API，  
用來預測鳶尾花（Iris）的三個品種：setosa、versicolor、virginica。

- 模型使用 scikit-learn 的 RandomForestClassifier 訓練，  
特徵為：sepal length、sepal width、petal length、petal width。

## 專案結構
```markdown
iris-api/
├── main.py             # FastAPI 主程式
├── train_iris.py       # 訓練並產生模型的腳本
├── models/
│   └── iris_model.pkl  # 訓練好的模型檔案
├── requirements.txt    # 所需 Python 套件
└── README.md           # 本說明文件
```

## 如何安裝與執行

### 1. 建立虛擬環境（建議使用 conda）

```
conda create -n iris-api python=3.11
conda activate iris-api
```

### 2. 安裝必要套件

```
# 先用 conda 安裝科學計算套件
conda install numpy scikit-learn -c conda-forge

# 再用 pip 安裝 web 相關套件
pip install -r requirements.txt
```

### 3. 產生模型（如果 models/ 資料夾裡沒有 iris_model.pkl）

```
python train_iris.py
```

### 4. 啟動 API 服務

```
uvicorn main:app --reload
```

服務預設會在 http://127.0.0.1:8000 啟動。

### 5. 打開互動式文件頁面

瀏覽器輸入以下網址：

```
http://127.0.0.1:8000/docs
```

你會看到 Swagger UI，可以直接測試 API。

## API 使用方式

### 健康檢查

- **方法**：GET
- **路徑**：`/health`
- **說明**：檢查服務與模型是否正常載入
- **回傳範例**：
  ```json
  {
    "status": "healthy",
    "model_loaded": true
  }
  ```

### 預測鳶尾花品種

- **方法**：POST
- **路徑**：`/predict`
- **請求格式**（JSON）：
  ```json
  {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }
  ```
- **回傳範例**：
  ```json
  {
    "prediction": "setosa",
    "probability": 1.0,
    "probabilities": [1.0, 0.0, 0.0]
  }
  ```

## 品種對應
- 0 → setosa
- 1 → versicolor
- 2 → virginica

## 線上部署版本（Render.com）

API 已成功部署到 Render.com，可直接透過網頁使用：

- **Swagger 互動文件**（推薦）：  
  https://iris-fastapi-n0v1.onrender.com/docs

- **健康檢查端點**：  
  https://iris-fastapi-n0v1.onrender.com/health

**注意**：  
使用免費方案，服務在長時間無人訪問後會自動休眠，第一次請求可能需要 10–60 秒喚醒。


---
最後更新：2026.02
```
