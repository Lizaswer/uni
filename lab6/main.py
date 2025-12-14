# main.py - Основное приложение
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session  # Исправлено: sqlalchemy, не sglalchemy
from typing import List
import json
import uvicorn

from database import SessionLocal, engine, Base
from models import Product, Order, OrderItem
from schemas import ProductCreate, ProductResponse, OrderCreate, OrderResponse
from rabbitmq_simulator import RabbitmqSimulator  # Исправлено: rabbitmq_simulator и RabbitmqSimulator

rabbiting = RabbitmqSimulator()  # Исправлено: RabbitmqSimulator

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Создаем FastAPI приложение
app = FastAPI(
    title="RabbitMQ Лабораторная работа",
    description="Система управления складом с RabbitMQ",
    version="1.0.0"
)

# Зависимость для работы с БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========== ОБРАБОТЧИКИ RABBITMQ ==========

def handle_product_message(message: str):
    """Обработчик сообщений о продуктах"""
    try:
        print(f"📦 Получено сообщение о продукте")
        
        # Парсим JSON
        data = json.loads(message) if isinstance(message, str) else message
        
        db = SessionLocal()
        try:
            product = Product(
                name=data.get("name", "Продукт"),
                price=data.get("price", 0),
                quantity=data.get("quantity", 0),
                category=data.get("category", "other"),
                status="in_stock"
            )
            db.add(product)
            db.commit()
            print(f"   ✅ Создан продукт: {product.name}")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            db.rollback()
        finally:
            db.close()
    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")

def handle_order_message(message: str):
    """Обработчик сообщений о заказах"""
    try:
        print(f"🛒 Получено сообщение о заказе")
        
        # Парсим JSON
        data = json.loads(message) if isinstance(message, str) else message
        
        db = SessionLocal()
        try:
            # Создаем заказ
            order = Order(
                customer_name=data.get("customer_name", "Клиент"),
                total_amount=data.get("total_amount", 0),
                status="completed"
            )
            db.add(order)
            db.commit()
            db.refresh(order)
            
            # Обрабатываем товары в заказе
            for item in data.get("items", []):
                product_id = item.get("product_id")
                quantity = item.get("quantity", 1)
                
                # Находим продукт
                product = db.query(Product).get(product_id)
                if product:
                    # Создаем элемент заказа
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product_id,
                        quantity=quantity,
                        price=item.get("price", product.price)
                    )
                    db.add(order_item)
                    
                    # Обновляем остатки
                    product.quantity -= quantity
                    if product.quantity <= 0:
                        product.quantity = 0
                        product.status = "out_of_stock"
            
            db.commit()
            print(f"   ✅ Создан заказ #{order.id}")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            db.rollback()
        finally:
            db.close()
    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")

# Подписываемся на очереди
rabbiting.queue_declare("product_queue")
rabbiting.queue_declare("order_queue")
rabbiting.basic_consume("product_queue", handle_product_message)
rabbiting.basic_consume("order_queue", handle_order_message)

# ========== API ENDPOINTS ==========

@app.get("/")
def root():
    return {
        "message": "Лабораторная работа №6: RabbitMQ",
        "endpoints": {
            "docs": "/docs",
            "products": "/products/",
            "orders": "/orders/",
            "test": "/test/send-products",
            "stats": "/rabbitmq/stats"
        }
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected",
        "rabbitmq": "simulator"
    }

@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Создать продукт через API"""
    db_product = Product(**product.dict())
    db_product.status = "in_stock" if db_product.quantity > 0 else "out_of_stock"
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """Получить все продукты"""
    return db.query(Product).all()

@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Создать заказ через API"""
    # Проверяем наличие товаров и считаем сумму
    total = 0
    for item in order.items:
        product = db.query(Product).get(item.product_id)
        if not product:
            raise HTTPException(400, f"Продукт {item.product_id} не найден")
        if product.quantity < item.quantity:
            raise HTTPException(400, f"Недостаточно {product.name}")
        total += product.price * item.quantity
    
    # Создаем заказ
    db_order = Order(
        customer_name=order.customer_name,
        total_amount=total,
        status="completed"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Создаем элементы заказа
    for item in order.items:
        product = db.query(Product).get(item.product_id)
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(order_item)
        
        # Обновляем остатки
        product.quantity -= item.quantity
        if product.quantity <= 0:
            product.status = "out_of_stock"
    
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    """Получить все заказы"""
    return db.query(Order).all()

@app.get("/rabbitmq/stats")
def get_rabbitmq_stats():
    """Получить статистику RabbitMQ"""
    return rabbitmq.get_stats()

@app.post("/test/send-products")
def send_test_products():
    """Отправить тестовые продукты в RabbitMQ"""
    products = [
        {"name": "Ноутбук Dell", "price": 85000, "quantity": 10, "category": "электроника"},
        {"name": "Мышь Logitech", "price": 2500, "quantity": 50, "category": "электроника"},
        {"name": "Клавиатура", "price": 4500, "quantity": 30, "category": "электроника"},
        {"name": "Монитор 24\"", "price": 30000, "quantity": 8, "category": "электроника"},
        {"name": "Наушники", "price": 8000, "quantity": 25, "category": "аудио"}
    ]
    
    for product in products:
        rabbitmq.basic_publish("", "product_queue", product)
    
    return {
        "status": "success",
        "message": "5 тестовых продуктов отправлены в RabbitMQ",
        "count": len(products)
    }

@app.post("/test/send-orders")
def send_test_orders():
    """Отправить тестовые заказы в RabbitMQ"""
    # Сначала проверим, есть ли продукты
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    
    if len(products) == 0:
        return {
            "error": "Сначала создайте продукты",
            "hint": "Используйте /test/send-products или /products/"
        }
    
    orders = [
        {
            "customer_name": "Иван Иванов",
            "total_amount": 87500,
            "items": [
                {"product_id": 1, "quantity": 1, "price": 85000},
                {"product_id": 2, "quantity": 1, "price": 2500}
            ]
        },
        {
            "customer_name": "Петр Петров",
            "total_amount": 34500,
            "items": [
                {"product_id": 3, "quantity": 1, "price": 4500},
                {"product_id": 4, "quantity": 1, "price": 30000}
            ]
        },
        {
            "customer_name": "Анна Сидорова",
            "total_amount": 8000,
            "items": [
                {"product_id": 5, "quantity": 1, "price": 8000}
            ]
        }
    ]
    
    for order in orders:
        rabbitmq.basic_publish("", "order_queue", order)
    
    return {
        "status": "success",
        "message": "3 тестовых заказа отправлены в RabbitMQ",
        "count": len(orders)
    }

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 ЗАПУСК ЛАБОРАТОРНОЙ РАБОТЫ №6")
    print("="*60)
    print("\n📊 Приложение доступно по адресам:")
    print("  • http://localhost:8000 - Главная страница")
    print("  • http://localhost:8000/docs - Документация API")
    print("\n🧪 Для тестирования используйте:")
    print("  • POST /test/send-products - отправить тестовые продукты")
    print("  • POST /test/send-orders - отправить тестовые заказы")
    print("  • GET /rabbitmq/stats - статистика RabbitMQ")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")