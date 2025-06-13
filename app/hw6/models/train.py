import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path

def train_models():
    data = pd.read_csv("raw_dataset.csv")
    X = data.drop("PurchaseStatus", axis=1)
    y = data["PurchaseStatus"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Простая модель
    model1 = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
    model1.fit(X_train, y_train)
    
    # Более сложная модель
    model2 = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    model2.fit(X_train, y_train)
    
    # Сохраняем модели
    Path("checkpoints").mkdir(exist_ok=True)
    joblib.dump(model1, "checkpoints/model1.joblib")
    joblib.dump(model2, "checkpoints/model2.joblib")
    
    return model1, model2

if __name__ == "__main__":
    train_models()