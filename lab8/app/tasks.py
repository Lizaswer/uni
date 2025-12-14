# app/tasks.py - периодические задачи для TaskIQ
from taskiq_aio_pika import AioPikaBroker
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
import datetime
from app.database import AsyncSessionLocal
from app.models import Report

# 1. Создаём брокер
broker = AioPikaBroker(
    "amqp://guest:guest@localhost:5672/",
    exchange_name="report",
    queue_name="cmd_order"
)

# 2. Создаём планировщик
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

# 3. Периодическая задача (каждую минуту)
@broker.task(
    schedule=[
        {
            "cron": "*/1 * * * *",  # Каждую минуту
            "args": [{
                "report_at": "2024-12-14",
                "order_id": 1,
                "count_product": 5
            }],
            "schedule_id": "generate_report_every_minute",
        }
    ]
)
async def generate_report(data: dict):
    """Задача, выполняемая каждую минуту для формирования отчёта"""
    
    print(f"📍 Создание отчёта: {data}")
    
    # Сохраняем в БД
    try:
        async with AsyncSessionLocal() as session:
            report = Report(
                report_at=datetime.date.today(),  # Используем сегодняшнюю дату
                order_id=data["order_id"],  # Берём как есть (уже int)
                count_product=data["count_product"]
            )
            session.add(report)
            await session.commit()
            await session.refresh(report)
            print(f"💾 Сохранено в БД: ID {report.id}")
            return {"status": "success", "db_id": report.id}
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        return {"status": "error", "message": str(e)}

# 4. Простая тестовая задача для ручного запуска
@broker.task
async def test_task(name: str) -> str:
    """Тестовая задача для проверки работы воркеров"""
    message = f"Привет, {name}! Задача выполнена."
    print(message)
    return message