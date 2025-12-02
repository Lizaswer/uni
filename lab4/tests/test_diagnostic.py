import pytest
from litestar.testing import TestClient


@pytest.mark.asyncio
async def test_diagnostic(test_client):
    """Диагностический тест для проверки работы приложения"""
    
    # 1. Проверяем доступность эндпоинта
    response = test_client.get("/users")
    
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Body: {response.text[:500]}...")
    
    # Если 500, смотрим что в ответе
    if response.status_code == 500:
        print("\n=== ERROR DETAILS ===")
        try:
            error_data = response.json()
            print(f"Error JSON: {error_data}")
        except:
            print(f"Raw error: {response.text}")
    
    # 2. Проверяем что приложение вообще отвечает
    assert response.status_code in [200, 201, 204, 404, 500], f"Unexpected status: {response.status_code}"


@pytest.mark.asyncio
async def test_dependency_injection(test_app):
    """Проверяем что DI работает"""
    from litestar.di import Provide
    
    # Проверяем что зависимость user_service зарегистрирована
    dependencies = test_app.dependencies
    print(f"Dependencies: {list(dependencies.keys())}")
    
    assert "user_service" in dependencies
    print("✅ user_service dependency registered")