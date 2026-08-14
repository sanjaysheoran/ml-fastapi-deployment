from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np

fastapi = FastAPI()

model = joblib.load("model.joblib")

class HouseFeatures(BaseModel):
    LiveArea: float = Field(..., ge=0, description="Live Area of the house in sqft")
    LotArea: float = Field(..., ge=0, description="Lot Area of the house in sqft")
    YrSold: int = Field(..., ge=1800, le=2100, description="Year the house was sold")

@fastapi.get("/health")
def health_check():
    return {"status":"healthy server"}

@fastapi.post("/predict")
def predict(payload: HouseFeatures):
    try:
        features = np.array([[payload.LiveArea, payload.LotArea, payload.YrSold]])
        prediction = model.predict(features)
        return {"predicted_price": prediction[0]}
    except Exception as e:
        raise HttpException(status_code=500, detail = str(e))

