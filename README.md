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

## Домашнее задание №6

### Запуск системы

1. Обучите модели:
```bash
python -m app.hw6.models.train
```

2. Запустите сервисы:
```bash
uvicorn app.hw6.app:create_app --reload
docker-compose -f docker-compose-hw6.yaml up -d
```

Доступные сервисы:
- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

### Собранные метрики

1. **Метрики запросов**:
   - `purchase_requests_total` — общее количество запросов к API покупок.

2. **Метрики CPU**:
   - `CPU Usage` — загрузка процессора.

### Настроенные алерты

1. **Алерт на высокое количество запросов**:
   - **Название**: `[FIRING] large number of requests`.
   - **Условие**: превышение порога (`B выше 1000`).

2. **Алерт на загрузку CPU**:
   - **Название**: `[FIRING] CPU low Load`.
   - **Условие**: низкая загрузка (`B ниже 80`).

### Скриншоты
Все скриншоты сохранены в папке `assets`.
