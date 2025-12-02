from unittest.mock import Mock

import pytest
from litestar.status_codes import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND)


class TestUserController:
    """Тесты для API endpoints пользователей"""
    
    @pytest.mark.asyncio
    async def test_get_all_users(self, test_client, mock_user_service):
        """Тест получения всех пользователей"""
        response = test_client.get("/users")
        
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        assert response.status_code == HTTP_200_OK, f"Expected 200, got {response.status_code}. Response: {response.text}"
        data = response.json()
        
        assert "users" in data
        assert data["total_count"] == 1
        assert len(data["users"]) == 1
        assert data["users"][0]["email"] == "test@example.com"
        
        mock_user_service.get_by_filter.assert_called_once()
        mock_user_service.get_total_count.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_user(self, test_client, mock_user_service):
        """Тест создания пользователя через API"""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "password123"
        }
        
        response = test_client.post("/users", json=user_data)
        
        print(f"Create user response: {response.status_code}")
        print(f"Response: {response.text}")
        
        assert response.status_code == HTTP_201_CREATED, f"Expected 201, got {response.status_code}"
        data = response.json()
        
        assert data["email"] == "test@example.com"  # Из мока
        assert data["username"] == "testuser"
        
        mock_user_service.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self, test_client, mock_user_service):
        """Тест получения пользователя по ID"""
        response = test_client.get("/users/1")
        
        assert response.status_code == HTTP_200_OK, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert data["id"] == 1
        assert data["email"] == "test@example.com"
        
        mock_user_service.get_by_id.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, test_client, mock_user_service):
        """Тест получения несуществующего пользователя"""
        # Настраиваем мок чтобы возвращал None
        mock_user_service.get_by_id.return_value = None
        
        response = test_client.get("/users/999")
        
        print(f"Not found response: {response.status_code}")
        print(f"Response: {response.text}")
        
        assert response.status_code == HTTP_404_NOT_FOUND, f"Expected 404, got {response.status_code}"
        
        mock_user_service.get_by_id.assert_called_once_with(999)
    
    @pytest.mark.asyncio
    async def test_delete_user(self, test_client, mock_user_service):
        """Тест удаления пользователя"""
        response = test_client.delete("/users/1")
        
        print(f"Delete response: {response.status_code}")
        
        # Проверяем что статус 204 No Content или 200 OK (в зависимости от реализации)
        assert response.status_code in [HTTP_204_NO_CONTENT, 200], f"Expected 204 or 200, got {response.status_code}"
        
        mock_user_service.delete.assert_called_once_with(1)