from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import pandas as pd

app = FastAPI()

# 解決跨域問題 (與原本設定一致)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. 載入模型與特徵清單
model = joblib.load('seoul_bike_model.joblib')
features_list = joblib.load('features_list.joblib')

# 2. 定義資料模型 (依照 train.py 中的 features 順序)
class BikeQuery(BaseModel):
    hour: int
    temp: float
    humidity: float
    wind_speed: float
    solar_rad: float
    rainfall: float
    snowfall: float
    seasons: int     # 0:Autumn, 1:Spring, 2:Summer, 3:Winter (依照 LabelEncoder 結果)
    holiday: int     # 0:Holiday, 1:No Holiday
    month: int
    day_of_week: int # 0:Mon, 6:Sun

@app.get("/")
def read_root():
    return {"message": "Seoul Bike Demand Prediction API is running"}

# 3. 預測路由
@app.post("/predict")
async def predict_bike(data: BikeQuery):
    # 將輸入轉換為模型需要的陣列格式
    # 順序必須與 features_list 一致
    input_features = np.array([[
        data.hour, data.temp, data.humidity, data.wind_speed,
        data.solar_rad, data.rainfall, data.snowfall,
        data.seasons, data.holiday, data.month, data.day_of_week
    ]])
    
    # 執行預測
    prediction = model.predict(input_features)[0]
    
    # 四捨五入並確保不小於 0
    final_count = max(0, int(round(prediction)))

    return {
        "predicted_count": final_count,
        "status": "success",
        "message": f"預測該時段租借需求量為 {final_count} 輛"
    }