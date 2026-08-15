from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np

#Create the object of FastAPI
fastapi = FastAPI()

#load the model from file
model = joblib.load("model.joblib")

#Create a class for the payload which will be accepted by predict
class HouseFeatures(BaseModel):
    LiveArea: float = Field(..., ge=0, description="Live Area of the house in sqft")
    LotArea: float = Field(..., ge=0, description="Lot Area of the house in sqft")
    YrSold: int = Field(..., ge=1800, le=2100, description="Year the house was sold")

#Endpoint for health check
@fastapi.get("/health")
def health_check():
    return {"status":"healthy server"}


#Endpoint for predicting the value based on input features
@fastapi.post("/predict")
def predict(payload: HouseFeatures):
    try:
        #read all the feature from the request payload
        features = np.array([[payload.LiveArea, payload.LotArea, payload.YrSold]])
        #predict the value based on input features
        prediction = model.predict(features)
        return {"predicted_price": prediction[0]}
    except Exception as e:
        raise HttpException(status_code=500, detail = str(e))

