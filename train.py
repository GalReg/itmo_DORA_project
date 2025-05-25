import warnings
import time
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd

# Подавление возможных предупреждений
warnings.filterwarnings("ignore")

def main():
    try:
        # Загрузка данных
        data = pd.read_csv('data/raw_dataset.csv')
        y = data['PurchaseStatus']
        X = data.drop('PurchaseStatus', axis=1)
        
        # Разделение на train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Список моделей для экспериментов
        models = {
            "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
            "LogisticRegression": LogisticRegression(max_iter=200, random_state=42),
            "SVM": SVC(probability=True, random_state=42)
        }

        # Настройка MLflow
        mlflow.set_experiment("Purchase Models Comparison")

        for model_name, model in models.items():
            with mlflow.start_run(run_name=model_name):
                print(f"Training {model_name}...")
                
                # Логируем параметры
                mlflow.log_param("model", model_name)
                
                # Обучение с замером времени
                start_time = time.time()
                model.fit(X_train, y_train)
                train_time = time.time() - start_time
                
                # Предсказание и метрики
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred, average='weighted')
                
                # Логируем метрики
                mlflow.log_metric("accuracy", accuracy)
                mlflow.log_metric("f1_score", f1)
                mlflow.log_metric("train_time", train_time)
                
                # Сохраняем модель
                mlflow.sklearn.log_model(model, model_name)
                
                print(f"{model_name} results:")
                print(f"Accuracy: {accuracy:.4f}")
                print(f"F1 Score: {f1:.4f}")
                print(f"Training Time: {train_time:.4f}s\n")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()