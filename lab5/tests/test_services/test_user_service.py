from unittest.mock import AsyncMock, Mock, patch

import pytest
from api.models.user import UserCreate, UserUpdate
from api.repositories.user_repository import UserRepository
from api.services.user_service import UserService


class TestUserService:
    """Тесты для сервиса пользователей"""
    
    @pytest.mark.asyncio
    async def test_create_user_success(self):
        """Тест успешного создания пользователя"""
        # Мокаем зависимости
        mock_repo = AsyncMock(spec=UserRepository)
        mock_session = AsyncMock()
        
        # Патчим метод get_by_email, который вызывается внутри сервиса
        with patch.object(UserService, 'get_by_email', new_callable=AsyncMock) as mock_get_by_email:
            mock_get_by_email.return_value = None  # Email не существует
            
            # Мок для создания пользователя
            mock_user = Mock()
            mock_user.id = 1
            mock_user.email = "test@example.com"
            mock_user.username = "testuser"
            mock_repo.create.return_value = mock_user
            
            # Создаем сервис с моками
            service = UserService(mock_repo, mock_session)
            
            # Патчим get_by_email внутри сервиса
            service.get_by_email = mock_get_by_email
            
            user_data = UserCreate(
                email="test@example.com",
                username="testuser",
                password="password123"
            )
            
            # Выполняем тест
            result = await service.create(user_data)
            
            # Проверяем результат
            assert result.id == 1
            assert result.email == "test@example.com"
            mock_repo.create.assert_called_once()
            mock_get_by_email.assert_called_once_with("test@example.com")
    
    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self):
        """Тест создания пользователя с дублирующимся email"""
        mock_repo = AsyncMock(spec=UserRepository)
        mock_session = AsyncMock()
        
        with patch.object(UserService, 'get_by_email', new_callable=AsyncMock) as mock_get_by_email:
            # Настраиваем мок для проверки существующего пользователя
            mock_user = Mock()
            mock_user.email = "existing@example.com"
            mock_get_by_email.return_value = mock_user
            
            service = UserService(mock_repo, mock_session)
            service.get_by_email = mock_get_by_email
            
            user_data = UserCreate(
                email="existing@example.com",  # Такой email уже существует
                username="newuser",
                password="password123"
            )
            
            # Ожидаем ошибку
            with pytest.raises(ValueError, match="User with email"):
                await service.create(user_data)
    
    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self):
        """Тест получения пользователя по ID"""
        mock_repo = AsyncMock(spec=UserRepository)
        mock_session = AsyncMock()
        
        mock_user = Mock()
        mock_user.id = 1
        mock_repo.get_by_id.return_value = mock_user
        
        service = UserService(mock_repo, mock_session)
        result = await service.get_by_id(1)
        
        assert result.id == 1
        mock_repo.get_by_id.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_user_not_found(self):
        """Тест обновления несуществующего пользователя"""
        mock_repo = AsyncMock(spec=UserRepository)
        mock_session = AsyncMock()
        
        mock_repo.get_by_id.return_value = None
        
        service = UserService(mock_repo, mock_session)
        update_data = UserUpdate(username="newusername")
        
        with pytest.raises(ValueError, match="not found"):
            await service.update(999, update_data)