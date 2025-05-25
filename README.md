# DORA project
MLOps course

## Workflow  
Мы используем **GitHub Flow**:  
1. `main` — стабильная ветка.  
2. Для задач создавайте ветки от `main`:  
   ```bash  
   git checkout -b feature/your-feature
3. Пушите изменения и создавайте PR.
  В PR обязательно:
  - Проверка линтерами.
  - Ревью кода.
4. После ревью мержите PR в main.

## Система версионирования

### Используемые инструменты
- **Git** - для кода и метаданных
- **DVC** - для данных и моделей
- **Google Drive/S3** - удалённое хранилище (через DVC)

### Рабочий процесс
1. Данные и модели добавляются через DVC:
   ```bash
   dvc add data/raw_dataset.csv
   dvc add models/random_forest.pkl
   ```
2. Фиксируются изменения в Git:
   ```bash
   git add data/raw_dataset.csv.dvc models/random_forest.pkl.dvc .gitignore
   git commit -m "Add raw dataset v1.0"
   ```
3. Отправляются в удалённое хранилище:
   ```bash
   dvc push
   ```

## Трекинг экспериментов с MLflow

MLflow используется для логирования параметров, метрик и артефактов экспериментов. Ниже приведено руководство по настройке и использованию.

### Настройка MLflow

1. **Установите MLflow**:
   ```bash
   pip install mlflow
   ```
   
2. **Добавьте в код трекинг**:
	```
	import mlflow

	mlflow.start_run()
	mlflow.log_param("param1", 42)  # Логируем параметры
	mlflow.log_metric("accuracy", 0.95)  # Логируем метрики
	mlflow.end_run()
	```
Запуск UI:
   ```bash
   mlflow ui --port 5000
   ```
Просмотр экспериментов: http://localhost:5000
