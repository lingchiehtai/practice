#自動處理 "SeoulBikeData.csv" 中的日期格式，並將季節、假日等文字轉換為機器學習能理解的數字 。
#訓練模型並導出 .joblib 模型檔

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

def train_bike_model():
    # 1. 讀取數據 (處理可能編碼問題)
    df = pd.read_csv('SeoulBikeData.csv', encoding='unicode_escape')
    
    # 2. 特徵工程 (Feature Engineering)
    # 將日期字串轉換為月份與週幾
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Month'] = df['Date'].dt.month
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    
    # 3. 類別資料轉碼 (Label Encoding)
    le = LabelEncoder()
    df['Seasons'] = le.fit_transform(df['Seasons'])      # Winter, Spring, etc.
    df['Holiday'] = le.fit_transform(df['Holiday'])      # Holiday, No Holiday
    df['Functioning Day'] = le.fit_transform(df['Functioning Day']) # Yes, No
    
    # 4. 定義特徵 (選取對預測最關鍵的欄位)
    # 我們選取：小時, 溫度, 濕度, 風速, 太陽輻射, 雨量, 雪量, 季節, 是否假日, 月份, 週幾
    features = [
        'Hour', 'Temperature(C)', 'Humidity(%)', 'Wind speed (m/s)', 
        'Solar Radiation (MJ/m2)', 'Rainfall(mm)', 'Snowfall (cm)', 
        'Seasons', 'Holiday', 'Month', 'DayOfWeek'
    ]
    
    X = df[features]
    y = df['Rented Bike Count'] # 目標值：租借數量
    
    # 5. 拆分訓練與測試集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 6. 訓練模型 (採用隨機森林回歸)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 7. 評估與保存
    score = model.score(X_test, y_test)
    print(f"模型訓練完成，R2 準確率為: {score:.4f}")
    
    # 保存模型供 FastAPI 使用
    joblib.dump(model, 'seoul_bike_model.joblib')
    # 同時保存特徵清單，確保 API 調用時順序一致
    joblib.dump(features, 'features_list.joblib')
    print("模型檔案已導出：seoul_bike_model.joblib")

if __name__ == "__main__":
    train_bike_model()