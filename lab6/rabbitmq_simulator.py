class RabbitmqSimulator:
    def __init__(self):
        # ИНИЦИАЛИЗИРУЕМ КАК СЛОВАРЬ, а не список!
        self.subscribers = {}  # Ключи: имена очередей, значения: списки подписчиков
        self.messages = []     # Список для хранения сообщений
        # Другие необходимые атрибуты...
    
    def queue_declare(self, queue_name):
        """Создать очередь, если она не существует"""
        if queue_name not in self.subscribers:
            self.subscribers[queue_name] = []  # Создаем пустой список для подписчиков этой очереди
            print(f"Очередь '{queue_name}' создана")
        else:
            print(f"Очередь '{queue_name}' уже существует")
    
    def basic_publish(self, exchange='', routing_key='', body=''):
        """Отправить сообщение в очередь"""
        # Здесь логика публикации сообщения
        message = {
            'exchange': exchange,
            'routing_key': routing_key,
            'body': body
        }
        self.messages.append(message)
        
        # Отправляем сообщение всем подписчикам указанной очереди
        if routing_key in self.subscribers:
            for subscriber in self.subscribers[routing_key]:
                # Здесь логика уведомления подписчиков
                pass
        
        print(f"Сообщение отправлено в очередь '{routing_key}': {body}")
    
    def basic_consume(self, queue='', on_message_callback=None):
        """Подписаться на очередь"""
        if queue not in self.subscribers:
            self.queue_declare(queue)  # Создаем очередь, если она не существует
        
        # Регистрируем callback-функцию как подписчика
        if on_message_callback:
            self.subscribers[queue].append(on_message_callback)
            print(f"Добавлен подписчик на очередь '{queue}'")
    