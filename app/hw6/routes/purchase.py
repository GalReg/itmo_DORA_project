from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from concurrent.futures import ProcessPoolExecutor
import asyncio
from functools import partial
from app.hw6.metrics import MODEL_USAGE
from app.hw6.models.model_loader import ModelRegistry

router = APIRouter(prefix="/purchase", tags=["purchase"])

def get_model_registry():
    return ModelRegistry()

class PurchaseFeatures(BaseModel):
    Age: int
    Gender: int
    AnnualIncome: float
    NumberOfPurchases: int
    ProductCategory: int
    TimeSpentOnWebsite: float
    LoyaltyProgram: int
    DiscountsAvailed: int

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    model_name: str

process_executor = ProcessPoolExecutor(max_workers=4)

@router.get("/models")
async def list_models(model_registry: ModelRegistry = Depends(get_model_registry)):
    return {"available_models": model_registry.get_available_models()}

@router.post("/predict/{model_name}", response_model=PredictionResponse)
async def predict(
    model_name: str,
    features: PurchaseFeatures,
    model_registry: ModelRegistry = Depends(get_model_registry)
):
    if model_name not in model_registry.get_available_models():
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")
    
    MODEL_USAGE.labels(model_name=model_name).inc()
    
    loop = asyncio.get_event_loop()
    prediction_func = partial(model_registry.predict, features.dict(), model_name)
    prediction, probability = await loop.run_in_executor(process_executor, prediction_func)
    
    return {
        "prediction": prediction,
        "probability": probability,
        "model_name": model_name
    }