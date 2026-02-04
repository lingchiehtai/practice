# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import numpy as np
from typing import List

app = FastAPI(title="Iris Prediction API", version="1.0")

#新增 CORS 中介層，讓它只允許特定的來源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 目前先用 *，測試完再改成特定網址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model (最關鍵)
model = None
class_names = ["setosa", "versicolor", "virginica"]

@app.on_event("startup")
async def load_model():
    global model
    try:
        with open("models/iris_model.pkl", "rb") as f:
            model = pickle.load(f)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Model load failed: {e}")

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
