from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.hw6.routes.purchase import router as purchase_router
from app.hw6.metrics import setup_metrics

def create_app() -> FastAPI:
    app = FastAPI(title="Purchase Prediction API")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(purchase_router)
    setup_metrics(app)
    
    return app