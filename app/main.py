from fastapi import FastAPI
from .models import load_model, predict
from .schemas import PredictionInput, PredictionOutput
import pandas as pd
from .config import settings

app = FastAPI(title="ML Model API")

# Загрузка модели при старте
model = load_model(settings.model_path)

@app.post("/predict", response_model=PredictionOutput)
async def make_prediction(input_data: PredictionInput):
    data = pd.DataFrame([input_data.dict()])
    prediction = predict(model, data)
    return {"prediction": prediction}