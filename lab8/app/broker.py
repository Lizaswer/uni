# app/broker.py
from taskiq_aio_pika import AioPikaBroker

broker = AioPikaBroker(
    "amqp://guest:guest@localhost:5672/",
    exchange_name="report",
    queue_name="cmd_order"
)

# Импортируем задачи из tasks.py
from app.tasks import generate_report, test_task