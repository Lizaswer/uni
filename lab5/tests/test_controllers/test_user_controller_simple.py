import pytest
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import TestClient


@pytest.mark.asyncio
async def test_get_all_users_simple(test_client):
    """Простой тест для GET /users"""
    response = test_client.get("/users")
    
    # Проверяем структуру ответа
    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert "users" in data
    assert "total_count" in data
    assert isinstance(data["users"], list)


@pytest.mark.asyncio 
async def test_create_user_simple(test_client, mock_user_service):
    """Простой тест для POST /users"""
    user_data = {
        "email": "new@example.com",
        "username": "newuser",
        "password": "password123"
    }
    
    # Настраиваем мок
    from unittest.mock import Mock
    mock_user = Mock()
    mock_user.id = 1
    mock_user.email = user_data["email"]
    mock_user.username = user_data["username"]
    mock_user.created_at = "2024-01-01T00:00:00"
    mock_user.updated_at = "2024-01-01T00:00:00"
    
    mock_user_service.create.return_value = mock_user
    
    response = test_client.post("/users", json=user_data)
    
    assert response.status_code == HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_get_user_by_id_simple(test_client, mock_user_service):
    """Простой тест для GET /users/{id}"""
    from unittest.mock import Mock
    mock_user = Mock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.username = "testuser"
    mock_user.created_at = "2024-01-01T00:00:00"
    mock_user.updated_at = "2024-01-01T00:00:00"
    
    mock_user_service.get_by_id.return_value = mock_user
    
    response = test_client.get("/users/1")
    
    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert data["id"] == 1