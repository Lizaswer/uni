import redis
import json

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(
            host=host, 
            port=port, 
            db=db, 
            decode_responses=True
        )
    
    def cache_user(self, user_id, user_data, ttl=3600):
        """Кэширование данных пользователя на 1 час по умолчанию"""
        key = f"user:{user_id}"
        self.client.setex(key, ttl, json.dumps(user_data))
        return True
    
    def get_user(self, user_id):
        """Получение пользователя из кэша"""
        key = f"user:{user_id}"
        data = self.client.get(key)
        return json.loads(data) if data else None
    
    def invalidate_user(self, user_id):
        """Удаление пользователя из кэша"""
        key = f"user:{user_id}"
        return self.client.delete(key)
    
    def cache_product(self, product_id, product_data, ttl=600):
        """Кэширование данных продукта на 10 минут по умолчанию"""
        key = f"product:{product_id}"
        self.client.setex(key, ttl, json.dumps(product_data))
        return True
    
    def update_product_cache(self, product_id, product_data):
        """Обновление кэша продукта"""
        return self.cache_product(product_id, product_data, ttl=600)

# Пример использования
if __name__ == "__main__":
    cache = RedisCache()
    
    # Кэширование пользователя
    user = {"id": 1, "name": "Иван Иванов", "email": "ivan@example.com"}
    cache.cache_user(1, user)
    
    # Получение из кэша
    cached_user = cache.get_user(1)
    print("Кэшированный пользователь:", cached_user)