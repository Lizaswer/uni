from typing import List, Optional

from api.models.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession

# Импортируем внутри функций или используем аннотации типов


class UserService:
    
    def __init__(self, user_repository, db_session: AsyncSession):
        # Используем строку вместо прямого импорта
        self.user_repository = user_repository
        self.db_session = db_session
    
    async def get_by_id(self, user_id: int) -> Optional["User"]:
        from api.models.user import User
        return await self.user_repository.get_by_id(self.db_session, user_id)
    
    async def get_by_email(self, email: str) -> Optional["User"]:
        from api.models.user import User
        from sqlalchemy import select
        
        result = await self.db_session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_by_filter(self, count: int = 10, page: int = 1, **kwargs) -> List["User"]:
        return await self.user_repository.get_by_filter(self.db_session, count, page, **kwargs)
    
    async def get_total_count(self, **kwargs) -> int:
        from api.models.user import User
        from sqlalchemy import func, select
        
        query = select(func.count(User.id))
        for key, value in kwargs.items():
            if hasattr(User, key) and value is not None:
                query = query.where(getattr(User, key) == value)
        
        result = await self.db_session.execute(query)
        return result.scalar() or 0
    
    async def create(self, user_data: UserCreate) -> "User":
        # Проверка уникальности email
        existing_user = await self.get_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"User with email {user_data.email} already exists")
        
        return await self.user_repository.create(self.db_session, user_data)
    
    async def update(self, user_id: int, user_data: UserUpdate) -> "User":
        # Проверка существования пользователя
        existing_user = await self.get_by_id(user_id)
        if not existing_user:
            raise ValueError(f"User with ID {user_id} not found")
        
        return await self.user_repository.update(self.db_session, user_id, user_data)
    
    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        await self.user_repository.delete(self.db_session, user_id)