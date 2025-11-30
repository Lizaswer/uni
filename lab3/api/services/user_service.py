from api.repositories.user_repository import UserRepository
from api.models.user import User, UserCreate, UserUpdate
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    
    def __init__(self, user_repository: UserRepository, db_session: AsyncSession):
        self.user_repository = user_repository
        self.db_session = db_session
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self.user_repository.get_by_id(self.db_session, user_id)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.user_repository.get_by_email(self.db_session, email)
    
    async def get_by_filter(self, count: int = 10, page: int = 1, **kwargs) -> List[User]:
        return await self.user_repository.get_by_filter(self.db_session, count, page, **kwargs)
    
    async def get_total_count(self, **kwargs) -> int:
        return await self.user_repository.get_total_count(self.db_session, **kwargs)
    
    async def create(self, user_data: UserCreate) -> User:
        # Проверка уникальности email
        existing_user = await self.get_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"User with email {user_data.email} already exists")
        
        # Проверка уникальности username
        users_with_username = await self.get_by_filter(username=user_data.username)
        if users_with_username:
            raise ValueError(f"User with username {user_data.username} already exists")
        
        return await self.user_repository.create(self.db_session, user_data)
    
    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        # Проверка существования пользователя
        existing_user = await self.get_by_id(user_id)
        if not existing_user:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Проверка уникальности email если он обновляется
        if user_data.email and user_data.email != existing_user.email:
            user_with_email = await self.get_by_email(user_data.email)
            if user_with_email:
                raise ValueError(f"User with email {user_data.email} already exists")
        
        # Проверка уникальности username если он обновляется
        if user_data.username and user_data.username != existing_user.username:
            users_with_username = await self.get_by_filter(username=user_data.username)
            if users_with_username:
                raise ValueError(f"User with username {user_data.username} already exists")
        
        return await self.user_repository.update(self.db_session, user_id, user_data)
    
    async def delete(self, user_id: int) -> None:
        await self.user_repository.delete(self.db_session, user_id)