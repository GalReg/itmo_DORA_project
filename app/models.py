import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time

def preprocess_data(df):
    # Минимальный препроцессинг
    X = df.drop('PurchaseStatus', axis=1)
    y = df['PurchaseStatus']
    return X, y

def train_and_save_models():
    df = pd.read_csv('data/raw_dataset.csv')
    X, y = preprocess_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Обучаем модели
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    joblib.dump(lr, 'models/logreg_v1.joblib')
    
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    joblib.dump(rf, 'models/rf_v1.joblib')
    
    # Оценка качества
    for name, model in [('Logistic Regression', lr), ('Random Forest', rf)]:
        start = time.time()
        preds = model.predict(X_test)
        duration = time.time() - start
        acc = accuracy_score(y_test, preds)
        print(f"{name} - Accuracy: {acc:.4f}, Time: {duration:.4f}s")

def load_model(model_path: str):
    return joblib.load(model_path)

def predict(model, data: pd.DataFrame):
    return int(model.predict(data)[0])