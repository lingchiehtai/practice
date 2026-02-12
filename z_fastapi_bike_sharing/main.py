from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import joblib
import numpy as np
import pandas as pd

app = FastAPI()

# 解決跨域問題 (與原本設定一致)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, #注意：當allow_origins使用 "*" 時，此項通常需設為 False
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

# @app.get("/")
# def read_root():
#     return {"message": "Seoul Bike Demand Prediction API is running"}
@app.get("/")
async def read_index():
    # 這會讓瀏覽器打開網址時，直接載入你的 HTML 檔案
    return FileResponse("index.html")

# 3. 預測路由
@app.post("/predict")
async def predict_bike(data: BikeQuery):
    print(f"收到預測請求: {data}")
    # 將 data 物件轉換成字典，並手動對應當初模型訓練時的欄位名稱
    input_dict = {
        "Hour": data.hour,
        "Temperature(C)": data.temp,
        "Humidity(%)": data.humidity,
        "Wind speed (m/s)": data.wind_speed,
        "Solar Radiation (MJ/m2)": data.solar_rad,
        "Rainfall(mm)": data.rainfall,
        "Snowfall (cm)": data.snowfall,
        "Seasons": data.seasons,
        "Holiday": data.holiday,
        "Month": data.month,
        "DayOfWeek": data.day_of_week
    }
    
    # 3. 轉換為 DataFrame
    input_df = pd.DataFrame([input_dict])
    
    # ✅ 新增：在 Logs 輸出輸入的資料（可選）
    print(f"--- 收到預測請求 ---")
    print(f"輸入特徵摘要: {input_dict}")

    # 4. 預測
    try:
        prediction = model.predict(input_df)[0]

        final_count = int(max(0, prediction))
        print(f"預測結果: {final_count} 輛")

        return {
            "predicted_count": final_count,
            "status": "success",
            "message": f"預測該時段租借需求量為 {final_count} 輛"
        }
    except Exception as e:
        print(f"❌ 預測出錯: {str(e)}")
        return {"status": "error", "message": str(e)}