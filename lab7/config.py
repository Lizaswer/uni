REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'decode_responses': True,
    'socket_connect_timeout': 5
}

CACHE_TTL = {
    'user': 3600,      # 1 час
    'product': 600,    # 10 минут
    'session': 1800    # 30 минут
}