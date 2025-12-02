from typing import List, Optional

import bcrypt
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

# Импортируем внутри функций если нужно
# from api.models.user import User, UserCreate, UserUpdate


class UserRepository:
    
    async def get_by_id(self, session: AsyncSession, user_id: int) -> Optional["User"]:
        from api.models.user import User
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, session: AsyncSession, email: str) -> Optional["User"]:
        from api.models.user import User
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_by_filter(self, session: AsyncSession, count: int = 10, page: int = 1, **kwargs) -> List["User"]:
        from api.models.user import User
        
        query = select(User)
        
        for key, value in kwargs.items():
            if hasattr(User, key) and value is not None:
                query = query.where(getattr(User, key) == value)
        
        offset = (page - 1) * count
        query = query.offset(offset).limit(count)
        
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_total_count(self, session: AsyncSession, **kwargs) -> int:
        from api.models.user import User
        
        query = select(func.count(User.id))
        
        for key, value in kwargs.items():
            if hasattr(User, key) and value is not None:
                query = query.where(getattr(User, key) == value)
        
        result = await session.execute(query)
        return result.scalar() or 0
    
    def _hash_password(self, password: str) -> str:
        """Хеширование пароля"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    async def create(self, session: AsyncSession, user_data: "UserCreate") -> "User":
        from api.models.user import User, UserCreate

        # Хеширование пароля
        hashed_password = self._hash_password(user_data.password)
        
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=hashed_password
        )
        
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def update(self, session: AsyncSession, user_id: int, user_data: "UserUpdate") -> "User":
        from api.models.user import User, UserUpdate
        
        user = await self.get_by_id(session, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'password' and value:
                setattr(user, 'password_hash', self._hash_password(value))
            elif hasattr(user, field) and value is not None:
                setattr(user, field, value)
        
        await session.commit()
        await session.refresh(user)
        return user
    
    async def delete(self, session: AsyncSession, user_id: int) -> None:
        user = await self.get_by_id(session, user_id)
        if user:
            await session.delete(user)
            await session.commit()