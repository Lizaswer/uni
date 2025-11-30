from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, selectinload
from database import User, Address

def query_related_data():
    # Подключаемся к БД
    engine = create_engine("sqlite:///lab2.db")
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        # Запрос пользователей с их адресами используя selectinload
        stmt = select(User).options(selectinload(User.addresses))
        users = session.execute(stmt).scalars().all()
        
        print("=== ПОЛЬЗОВАТЕЛИ С АДРЕСАМИ ===")
        for user in users:
            print(f"👤 Пользователь: {user.username} ({user.email})")
            print("📍 Адреса:")
            for address in user.addresses:
                print(f"   - {address.street}, {address.city}, {address.country}")
            print("-" * 50)

if __name__ == "__main__":
    query_related_data()