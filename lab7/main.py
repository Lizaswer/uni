import redis

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def test_connection():
    try:
        r.ping()
        print("✅ Успешное подключение к Redis")
    except redis.ConnectionError:
        print("❌ Ошибка подключения к Redis")

def demonstrate_strings():
    print("\n=== Работа со строками ===")
    r.set("user:name", "Иван")
    print("Имя пользователя:", r.get("user:name"))
    
    r.setex("session:123", 10, "active")  # TTL 10 секунд для демо
    print("Сессия:", r.get("session:123"))
    
    r.set("counter", 0)
    r.incr("counter")
    r.incrby("counter", 5)
    print("Счетчик:", r.get("counter"))

def demonstrate_lists():
    print("\n=== Работа со списками ===")
    r.delete("tasks")  # Очистка перед началом
    r.lpush("tasks", "task1", "task2")
    r.rpush("tasks", "task3", "task4")
    print("Все задачи:", r.lrange("tasks", 0, -1))
    print("Длина списка:", r.llen("tasks"))

def demonstrate_sets():
    print("\n=== Работа с множествами ===")
    r.sadd("tags", "python", "redis", "database")
    r.sadd("languages", "python", "java", "javascript")
    print("Все теги:", r.smembers("tags"))
    print("Пересечение:", r.sinter("tags", "languages"))

def demonstrate_hashes():
    print("\n=== Работа с хэшами ===")
    r.hset("user:1000", mapping={"name": "Иван", "age": "30", "city": "Москва"})
    print("Данные пользователя:", r.hgetall("user:1000"))
    print("Имя:", r.hget("user:1000", "name"))

def demonstrate_sorted_sets():
    print("\n=== Работа с упорядоченными множествами ===")
    r.zadd("leaderboard", {"player1": 100, "player2": 200, "player3": 150})
    print("Топ-3 игрока:", r.zrange("leaderboard", 0, 2, withscores=True))
    print("Ранг player1:", r.zrank("leaderboard", "player1"))

def cache_demo():
    print("\n=== Демонстрация кэширования ===")
    # Кэширование пользователя на 5 секунд (для демо)
    user_data = '{"id": 1, "name": "Иван", "email": "ivan@example.com"}'
    r.setex("cached:user:1", 5, user_data)
    print("Данные в кэше:", r.get("cached:user:1"))
    
    # Очистка кэша
    r.delete("cached:user:1")
    print("После удаления:", r.get("cached:user:1"))

if __name__ == "__main__":
    test_connection()
    demonstrate_strings()
    demonstrate_lists()
    demonstrate_sets()
    demonstrate_hashes()
    demonstrate_sorted_sets()
    cache_demo()