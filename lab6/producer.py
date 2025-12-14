# producer.py - Тестовый продюсер
import requests
import time
import json

print("="*60)
print("🧪 ТЕСТИРОВАНИЕ RABBITMQ - ЛАБОРАТОРНАЯ РАБОТА 6")
print("="*60)

def main():
    base_url = "http://localhost:8000"
    
    print("\n1. Проверка подключения к серверу...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ Сервер работает")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            return
    except:
        print(f"   ❌ Не удалось подключиться к {base_url}")
        print("   Запустите сначала сервер: python main.py")
        return
    
    print("\n2. Отправляем тестовые продукты через RabbitMQ...")
    response = requests.post(f"{base_url}/test/send-products")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ {result['message']}")
        print(f"   📊 Количество: {result['count']}")
    else:
        print(f"   ❌ Ошибка: {response.text}")
        return
    
    print("\n3. Ждем обработки продуктов (2 секунды)...")
    time.sleep(2)
    
    print("\n4. Проверяем созданные продукты...")
    response = requests.get(f"{base_url}/products/")
    if response.status_code == 200:
        products = response.json()
        print(f"   ✅ Продуктов в базе: {len(products)}")
        for p in products:
            print(f"      • {p['name']} - {p['price']} руб. (остаток: {p['quantity']})")
    else:
        print(f"   ❌ Ошибка: {response.text}")
    
    print("\n5. Отправляем тестовые заказы через RabbitMQ...")
    response = requests.post(f"{base_url}/test/send-orders")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ {result['message']}")
        print(f"   📊 Количество: {result['count']}")
    else:
        print(f"   ❌ Ошибка: {response.text}")
        return
    
    print("\n6. Ждем обработки заказов (2 секунды)...")
    time.sleep(2)
    
    print("\n7. Проверяем созданные заказы...")
    response = requests.get(f"{base_url}/orders/")
    if response.status_code == 200:
        orders = response.json()
        print(f"   ✅ Заказов в базе: {len(orders)}")
        for o in orders:
            print(f"      • Заказ #{o['id']}: {o['customer_name']} - {o['total_amount']} руб.")
    else:
        print(f"   ❌ Ошибка: {response.text}")
    
    print("\n8. Получаем статистику RabbitMQ...")
    response = requests.get(f"{base_url}/rabbitmq/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"   📊 Статистика:")
        print(f"      • Очередей: {len(stats['queues'])}")
        print(f"      • Всего сообщений: {stats['total_messages']}")
        print(f"      • Подписчиков: {stats['total_subscribers']}")
        
        if stats['recent_messages']:
            print(f"      • Последние сообщения:")
            for msg in stats['recent_messages']:
                print(f"        [{msg['time']}] {msg['queue']}: {msg['message']}")
    
    print("\n" + "="*60)
    print("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
    print("="*60)
    
    print("\n📋 ДЛЯ ПРОВЕРКИ ОТКРОЙТЕ В БРАУЗЕРЕ:")
    print(f"   • {base_url} - Главная страница")
    print(f"   • {base_url}/docs - Документация API")
    print(f"   • {base_url}/products/ - Список продуктов")
    print(f"   • {base_url}/orders/ - Список заказов")

if __name__ == "__main__":
    main()