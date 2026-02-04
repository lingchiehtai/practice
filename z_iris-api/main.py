# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import numpy as np
from typing import List
import os
from contextlib import asynccontextmanager

# 定義全域變數
# Global model (最關鍵)
model = None
class_names = ["setosa", "versicolor", "virginica"]


#先定義 lifespan（放在 app 建立之前）
@asynccontextmanager 
async def lifespan(app: FastAPI):
#async def load_model():
    # startup 事件：這裡放原本的載入模型邏輯
    global model
    try:
        model_path = os.getenv("MODEL_PATH", "models/iris_model.pkl")  # 預設值仍是原本路徑
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Model load failed: {e}")
    yield  # ← 這行很重要，表示應用程式開始運行
    # shutdown 事件：這裡可以放清理資源的程式碼（目前可留空）
    print("Shutting down...")

#建立 app 的位置
app = FastAPI(
    title="Iris Prediction API", 
    version="1.0",
    lifespan=lifespan   # ← 關鍵：把 lifespan 綁定進來
)

#新增 CORS 中介層，讓它只允許特定的來源
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # 如果你有本地前端(前端常見的本地測試port)
        "http://127.0.0.1:3000",
        # "https://你的前端網址.com",   # 等上線時再加進去
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




class PredictionRequest(BaseModel):
    sepal_length: float = Field(..., gt=0, le=10)
    sepal_width: float = Field(..., gt=0, le=10)
    petal_length: float = Field(..., gt=0, le=10)
    petal_width: float = Field(..., gt=0, le=10)

class PredictionResponse(BaseModel):
    prediction: str
    probability: float
    probabilities: List[float]

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
async def predict(data: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    input_data = np.array([[data.sepal_length, data.sepal_width, 
                          data.petal_length, data.petal_width]])
    
    pred_class = model.predict(input_data)[0]
    probas = model.predict_proba(input_data)[0]
    max_prob = float(max(probas))
    
    return {
        "prediction": class_names[pred_class],
        "probability": max_prob,
        "probabilities": [round(p, 4) for p in probas]
    }
