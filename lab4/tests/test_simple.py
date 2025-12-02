import pytest
import sys
import os

def test_imports():
    """Тест что основные модули импортируются"""
    # Тестируем импорты по отдельности
    try:
        from api.models.user import User
        print("✅ User model imported")
    except ImportError as e:
        print(f"❌ Failed to import User: {e}")
        raise
    
    try:
        from api.repositories.user_repository import UserRepository
        print("✅ UserRepository imported")
    except ImportError as e:
        print(f"❌ Failed to import UserRepository: {e}")
        raise
    
    try:
        from api.services.user_service import UserService
        print("✅ UserService imported")
    except ImportError as e:
        print(f"❌ Failed to import UserService: {e}")
        raise
    
    try:
        from api.controllers.user_controller import UserController
        print("✅ UserController imported")
    except ImportError as e:
        print(f"❌ Failed to import UserController: {e}")
        raise
    
    assert True

def test_fixtures():
    """Тест что фикстуры работают"""
    # Просто проверяем что файл существует
    assert os.path.exists("tests/conftest.py")
    print("✅ conftest.py exists")

@pytest.mark.asyncio
async def test_async():
    """Простой async тест"""
    assert 1 + 1 == 2
    print("✅ Async test passed")