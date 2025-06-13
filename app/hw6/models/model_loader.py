import joblib
from pathlib import Path

class ModelRegistry:
    def __init__(self):
        self.models = {}
        self.load_models()
    
    def load_models(self):
        models_dir = Path("checkpoints")
        for model_file in models_dir.glob("*.joblib"):
            model_name = model_file.stem
            self.models[model_name] = joblib.load(model_file)
    
    def get_available_models(self):
        return list(self.models.keys())
    
    def predict(self, features: dict, model_name: str):
        model = self.models.get(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        
        # Преобразование features в правильный формат
        features_array = [[
            features["Age"],
            features["Gender"],
            features["AnnualIncome"],
            features["NumberOfPurchases"],
            features["ProductCategory"],
            features["TimeSpentOnWebsite"],
            features["LoyaltyProgram"],
            features["DiscountsAvailed"]
        ]]
        
        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0][1]
        
        return prediction, probability