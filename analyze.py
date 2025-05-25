import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
from sklearn.metrics import classification_report

client = MlflowClient()

# Получаем данные о последних запусках
experiment = client.get_experiment_by_name("Purchase Models Comparison")
runs = client.search_runs(experiment.experiment_id)

# Собираем метрики
results = []
for run in runs:
    model_name = run.data.params['model']
    accuracy = run.data.metrics['accuracy']
    f1 = run.data.metrics['f1_score']
    train_time = run.data.metrics['train_time']
    
    # Загружаем модель для дополнительных метрик
    model = mlflow.sklearn.load_model(f"runs:/{run.info.run_id}/{model_name}")
    
    results.append({
        'Model': model_name,
        'Accuracy': accuracy,
        'F1 Score': f1,
        'Training Time': train_time
    })

# Создаем отчет
report = pd.DataFrame(results).sort_values('Accuracy', ascending=False)
print(report)

# Сохраняем отчет в markdown
with open("report.md", "w") as f:
    f.write("# Сравнение моделей на Purchase dataset\n\n")
    f.write(report.to_markdown(index=False))
