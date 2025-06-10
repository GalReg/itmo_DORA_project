import requests
import pandas as pd
import time
import json
import os
from pathlib import Path
from datetime import datetime
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from app.config import settings

def test_api():
    # Загрузка тестовых данных
    data_path = Path(__file__).parent.parent / "data" / "raw_dataset.csv"
    df = pd.read_csv(data_path)
    
    # Подготовка данных
    test_data = df.drop('PurchaseStatus', axis=1).to_dict('records')
    y_true = df['PurchaseStatus'].tolist()
    
    # URL API (может быть изменен для Docker)
    API_URL = "http://localhost:8000/predict"
    
    # Сбор метрик
    times = []
    y_pred = []
    total = len(test_data)
    
    print(f"Starting API testing for model: {os.path.basename(settings.model_path)}")
    print(f"Total test samples: {total}")
    
    # Отправка запросов
    for i, data in enumerate(test_data, 1):
        try:
            start = time.time()
            response = requests.post(API_URL, json=data)
            duration = time.time() - start
            times.append(duration)
            
            if response.status_code == 200:
                pred = response.json()['prediction']
                y_pred.append(pred)
            else:
                print(f"Error in request {i}: {response.status_code}")
                y_pred.append(-1)  # Маркер ошибки
            
            if i % 10 == 0:
                print(f"Processed {i}/{total} requests...")
                
        except Exception as e:
            print(f"Exception on request {i}: {str(e)}")
            times.append(0)  # Чтобы не сбить статистику
            y_pred.append(-1)
    
    # Расчет метрик (только для успешных предсказаний)
    valid_preds = [pred for pred in y_pred if pred != -1]
    valid_true = [true for pred, true in zip(y_pred, y_true) if pred != -1]
    
    # Генерация отчета
    report = {
        "model": os.path.basename(settings.model_path),
        "test_date": datetime.now().isoformat(),
        "total_requests": total,
        "successful_requests": len(valid_preds),
        "error_rate": (total - len(valid_preds)) / total,
        "accuracy": accuracy_score(valid_true, valid_preds),
        "precision": precision_score(valid_true, valid_preds),
        "recall": recall_score(valid_true, valid_preds),
        "f1_score": f1_score(valid_true, valid_preds),
        "avg_time": sum(times) / len(times),
        "min_time": min(times),
        "max_time": max(times),
        "throughput": len(times) / sum(times) if sum(times) > 0 else 0
    }
    
    # Сохранение отчета
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    model_name = os.path.basename(settings.model_path).replace(".joblib", "")
    report_path = reports_dir / f"report_{model_name}.json"
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\nTest completed!")
    print(f"Report saved to: {report_path}")
    print("\nMetrics summary:")
    print(f"Accuracy: {report['accuracy']:.4f}")
    print(f"Avg time: {report['avg_time']:.4f}s")
    print(f"Throughput: {report['throughput']:.2f} requests/sec")

if __name__ == "__main__":
    test_api()