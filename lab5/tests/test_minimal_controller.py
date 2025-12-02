from unittest.mock import AsyncMock, Mock

import pytest
from litestar import Litestar, get, post
from litestar.di import Provide
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import TestClient


# 1. Создаем минимальный контроллер для теста
@get("/test")
async def get_test(service: AsyncMock) -> dict:
    return {"message": "test", "service_called": service.was_called}


@post("/test")
async def post_test(service: AsyncMock, data: dict) -> dict:
    return {"message": "created", "data": data, "service_called": service.was_called}


# 2. Тест
@pytest.mark.asyncio
async def test_minimal_controller():
    """Минимальный тест контроллера"""
    
    # Создаем мок сервиса
    mock_service = AsyncMock()
    mock_service.was_called = True
    
    async def provide_service() -> AsyncMock:
        return mock_service
    
    # Создаем минимальное приложение
    app = Litestar(
        route_handlers=[get_test, post_test],
        dependencies={
            "service": Provide(provide_service, sync_to_thread=False),
        }
    )
    
    # Тестируем
    with TestClient(app=app) as client:
        # GET запрос
        response = client.get("/test")
        print(f"GET Response: {response.status_code} - {response.json()}")
        assert response.status_code == HTTP_200_OK
        
        # POST запрос
        response = client.post("/test", json={"test": "data"})
        print(f"POST Response: {response.status_code} - {response.json()}")
        assert response.status_code == HTTP_201_CREATED
    
    print("✅ Минимальный тест контроллера прошел успешно!")


# 3. Тест с UserController
@pytest.mark.asyncio
async def test_user_controller_minimal():
    """Минимальный тест UserController"""
    from api.controllers.user_controller import UserController

    # Мок сервиса
    mock_service = AsyncMock()
    mock_user = Mock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.username = "testuser"
    mock_user.created_at = "2024-01-01T00:00:00"
    mock_user.updated_at = "2024-01-01T00:00:00"
    
    mock_service.get_by_filter.return_value = [mock_user]
    mock_service.get_total_count.return_value = 1
    
    async def provide_user_service() -> AsyncMock:
        return mock_service
    
    # Создаем приложение ТОЛЬКО с UserController
    app = Litestar(
        route_handlers=[UserController],
        dependencies={
            "user_service": Provide(provide_user_service, sync_to_thread=False),
        },
        debug=False
    )
    
    with TestClient(app=app) as client:
        response = client.get("/users")
        print(f"\n=== UserController Test ===")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        # Проверяем что не 500
        assert response.status_code != 500, f"Got 500 error: {response.text}"
        
        # Если 200, проверяем структуру
        if response.status_code == 200:
            data = response.json()
            print(f"Data keys: {list(data.keys())}")
            assert "users" in data
    
    print("✅ UserController тест прошел!")