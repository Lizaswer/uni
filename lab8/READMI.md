# Лабораторная работа №8: TaskIQ и планировщики задач

## Запуск проекта

# 1. Установка зависимости:
```bash
pip install -r requirements.txt

# 2. Запуск RabbitMQ и PostgreSQL:

docker-compose up -d

# 3. Создание таблицы в БД

python -c "from app.database import engine; from app.models import Base; import asyncio; asyncio.run(Base.metadata.create_all(bind=engine))"

# 4. Запуск FastAP приложение

python run.py

#5. В отдельном терминале запуск воркера TaskIQ

taskiq worker app.broker:broker

#6. В другом терминале запустите планировщик:

taskiq scheduler app.broker:scheduler --skip-first-run

