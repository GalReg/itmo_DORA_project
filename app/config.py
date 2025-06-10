from pydantic import BaseSettings

class Settings(BaseSettings):
    model_path: str = "models/logreg_v1.joblib"
    
    class Config:
        env_file = ".env"

settings = Settings()