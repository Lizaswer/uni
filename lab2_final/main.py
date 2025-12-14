# main.py
import os

from queries import query_related_data
from seed_data import seed_initial_data


def main():
    print("🚀 ЛАБОРАТОРНАЯ РАБОТА №2: SQLAlchemy и Alembic")
    print("=" * 50)
    
    # Проверяем существование БД
    if not os.path.exists("lab2.db"):
        print("❌ База данных не найдена! Сначала выполните миграции.")
        return
    
    # Показываем меню
    while True:
        print("\nВыберите действие:")
        print("1 - Наполнить БД тестовыми данными")
        print("2 - Вывести связанные данные")
        print("3 - Выйти")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == "1":
            print("\n📥 Наполняем БД данными...")
            seed_initial_data()
        elif choice == "2":
            print("\n📊 Выводим связанные данные...")
            query_related_data()
        elif choice == "3":
            print("👋 Выход из программы")
            break
        else:
            print("❌ Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    main()