from database import Address, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def seed_initial_data():
    # Создаем фабрику подключений
    engine = create_engine(
        "sqlite:///lab2.db",
        echo=True  # Логирование SQL-запросов
    )
    
    # Создаем фабрику сессий
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        # Создаем 5 пользователей
        users_data = [
            {"username": "john_doe", "email": "john@example.com"},
            {"username": "jane_smith", "email": "jane@example.com"},
            {"username": "bob_wilson", "email": "bob@example.com"},
            {"username": "alice_brown", "email": "alice@example.com"},
            {"username": "charlie_davis", "email": "charlie@example.com"}
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"]
            )
            users.append(user)
            session.add(user)
        
        session.commit()
        print("✅ Пользователи созданы")
        
        # Создаем адреса для пользователей
        addresses_data = [
            {"user": users[0], "street": "123 Main St", "city": "New York", "country": "USA", "is_primary": True},
            {"user": users[1], "street": "456 Oak Ave", "city": "Los Angeles", "country": "USA", "is_primary": True},
            {"user": users[2], "street": "789 Pine Rd", "city": "Chicago", "country": "USA", "is_primary": True},
            {"user": users[3], "street": "321 Elm St", "city": "Miami", "country": "USA", "is_primary": True},
            {"user": users[4], "street": "654 Maple Dr", "city": "Seattle", "country": "USA", "is_primary": True}
        ]
        
        for addr_data in addresses_data:
            address = Address(
                user_id=addr_data["user"].id,
                street=addr_data["street"],
                city=addr_data["city"],
                country=addr_data["country"],
                is_primary=addr_data["is_primary"]
            )
            session.add(address)
        
        session.commit()
        print("✅ Адреса созданы")
        print("🎉 База данных успешно наполнена тестовыми данными!")

if __name__ == "__main__":
    seed_initial_data()