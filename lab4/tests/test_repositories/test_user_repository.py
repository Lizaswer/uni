import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from api.repositories.user_repository import UserRepository
from api.models.user import UserCreate, UserUpdate


class TestUserRepository:
    """Тесты для репозитория пользователей"""
    
    @pytest.mark.asyncio
    async def test_create_user(self, session: AsyncSession, user_repository: UserRepository):
        """Тест создания пользователя"""
        user_data = UserCreate(
            email="test@example.com",
            username="testuser",
            password="password123"
        )
        
        user = await user_repository.create(session, user_data)
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.password_hash is not None
    
    @pytest.mark.asyncio
    async def test_get_by_id(self, session: AsyncSession, user_repository: UserRepository):
        """Тест получения пользователя по ID"""
        # Сначала создаем пользователя
        user_data = UserCreate(
            email="getbyid@example.com",
            username="getbyid",
            password="password123"
        )
        created_user = await user_repository.create(session, user_data)
        
        # Получаем пользователя по ID
        found_user = await user_repository.get_by_id(session, created_user.id)
        
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == created_user.email
    
    @pytest.mark.asyncio
    async def test_get_by_filter(self, session: AsyncSession, user_repository: UserRepository):
        """Тест получения пользователей с фильтрацией"""
        # Создаем нескольких пользователей
        users_data = [
            UserCreate(email=f"user{i}@example.com", username=f"user{i}", password="pass")
            for i in range(5)
        ]
        
        for user_data in users_data:
            await user_repository.create(session, user_data)
        
        # Тестируем пагинацию
        users_page1 = await user_repository.get_by_filter(session, count=2, page=1)
        users_page2 = await user_repository.get_by_filter(session, count=2, page=2)
        
        assert len(users_page1) == 2
        assert len(users_page2) == 2
        assert users_page1[0].id != users_page2[0].id
    
    @pytest.mark.asyncio
    async def test_update_user(self, session: AsyncSession, user_repository: UserRepository):
        """Тест обновления пользователя"""
        # Создаем пользователя
        user_data = UserCreate(
            email="update@example.com",
            username="updateuser",
            password="password123"
        )
        user = await user_repository.create(session, user_data)
        
        # Обновляем пользователя
        update_data = UserUpdate(username="updatedusername", email="updated@example.com")
        updated_user = await user_repository.update(session, user.id, update_data)
        
        assert updated_user.username == "updatedusername"
        assert updated_user.email == "updated@example.com"
    
    @pytest.mark.asyncio
    async def test_delete_user(self, session: AsyncSession, user_repository: UserRepository):
        """Тест удаления пользователя"""
        # Создаем пользователя
        user_data = UserCreate(
            email="delete@example.com",
            username="deleteuser",
            password="password123"
        )
        user = await user_repository.create(session, user_data)
        
        # Удаляем пользователя
        await user_repository.delete(session, user.id)
        
        # Проверяем что пользователь удален
        deleted_user = await user_repository.get_by_id(session, user.id)
        assert deleted_user is None