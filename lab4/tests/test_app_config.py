import pytest
from app.main import create_app
from litestar.testing import TestClient


@pytest.mark.asyncio
async def test_main_app():
    """Тест основного приложения из app/main.py"""
    
    # Убедимся что в тестовом режиме
    import os
    os.environ["TESTING"] = "1"
    
    app = create_app()
    
    with TestClient(app=app) as client:
        response = client.get("/users")
        print(f"\n=== Main App Test ===")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 500:
            print(f"Error: {response.text}")
        
        # Главное - не 500
        assert response.status_code != 500, f"Main app returns 500: {response.text}"
        
        # Может быть 200 (если зависимости настроены) или другая ошибка
        print(f"Response OK: {response.status_code}")


@pytest.mark.asyncio 
async def test_app_structure():
    """Проверка структуры приложения"""
    from app.main import app
    
    print(f"\n=== App Structure ===")
    print(f"Route handlers: {len(app.route_handlers)}")
    
    for handler in app.route_handlers:
        print(f"  - {handler}")
    
    print(f"Dependencies: {list(app.dependencies.keys())}")
    
    assert "user_service" in app.dependencies
    print("✅ user_service dependency found in main app")