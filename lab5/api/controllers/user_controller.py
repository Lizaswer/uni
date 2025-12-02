from typing import Any, Dict, List

from api.models.user import UserCreate, UserResponse, UserUpdate
from api.services.user_service import UserService
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.params import Parameter
from litestar.status_codes import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT)


class UserController(Controller):
    path = "/users"
    
    @get("/{user_id:int}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: int = Parameter(gt=0),
    ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)
    
    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = Parameter(gt=0, le=100, default=10),
        page: int = Parameter(gt=0, default=1)
    ) -> Dict[str, Any]:
        """Получить всех пользователей с пагинацией"""
        users = await user_service.get_by_filter(count=count, page=page)
        total_count = await user_service.get_total_count()
        
        return {
            "users": [UserResponse.model_validate(user) for user in users],
            "total_count": total_count,
            "page": page,
            "count": count,
            "total_pages": (total_count + count - 1) // count if count > 0 else 0
        }
    
    @post(status_code=HTTP_201_CREATED)
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserResponse:
        """Создать нового пользователя"""
        try:
            user = await user_service.create(data)
            return UserResponse.model_validate(user)
        except ValueError as e:
            raise NotFoundException(detail=str(e))
    
    @delete("/{user_id:int}", status_code=HTTP_204_NO_CONTENT)
    async def delete_user(
        self,
        user_service: UserService,
        user_id: int,
    ) -> None:
        """Удалить пользователя по ID"""
        try:
            await user_service.delete(user_id)
        except ValueError as e:
            raise NotFoundException(detail=str(e))
    
    @put("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: int,
        data: UserUpdate,
    ) -> UserResponse:
        """Обновить пользователя"""
        try:
            user = await user_service.update(user_id, data)
            return UserResponse.model_validate(user)
        except ValueError as e:
            raise NotFoundException(detail=str(e))