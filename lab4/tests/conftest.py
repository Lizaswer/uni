import sys
import os
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from litestar import Litestar
from litestar.di import Provide
from unittest.mock import AsyncMock, Mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

Base = declarative_base()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="session")
async def setup_database(engine):
    from api.models.user import Base as UserBase
    async with engine.begin() as conn:
        await conn.run_sync(UserBase.metadata.drop_all)
        await conn.run_sync(UserBase.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(UserBase.metadata.drop_all)

@pytest.fixture
async def session(engine, setup_database) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def user_repository(session):
    from api.repositories.user_repository import UserRepository
    return UserRepository()

@pytest.fixture
async def user_service(user_repository, session):
    from api.services.user_service import UserService
    return UserService(user_repository, session)

# ===== ВАЖНО: Обновленные фикстуры для контроллеров =====

@pytest.fixture
def mock_user_service():
    """Мок сервиса пользователей"""
    mock = AsyncMock()
    
    # Настраиваем возвращаемые значения для всех методов
    mock_user = Mock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.username = "testuser"
    mock_user.created_at = "2024-01-01T00:00:00"
    mock_user.updated_at = "2024-01-01T00:00:00"
    
    mock.get_by_filter.return_value = [mock_user]
    mock.get_total_count.return_value = 1
    mock.get_by_id.return_value = mock_user
    mock.create.return_value = mock_user
    mock.update.return_value = mock_user
    mock.delete.return_value = None
    
    return mock

@pytest.fixture
def test_app(mock_user_service):
    """Приложение с мокнутыми зависимостями"""
    from api.controllers.user_controller import UserController
    
    async def provide_user_service() -> AsyncMock:
        return mock_user_service
    
    # Создаем приложение ТОЛЬКО с необходимыми зависимостями
    # UserController ожидает user_service, но не ожидает db_session или user_repository
    app = Litestar(
        route_handlers=[UserController],
        dependencies={
            "user_service": Provide(provide_user_service, sync_to_thread=False),
        },
        debug=True  # Включаем debug для лучших сообщений об ошибках
    )
    return app

@pytest.fixture
def test_client(test_app):
    """TestClient с настроенным приложением"""
    from litestar.testing import TestClient
    return TestClient(app=test_app)

# Альтернативная фикстура для приложения с реальными зависимостями
@pytest.fixture
def real_test_app(user_service):
    """Приложение с реальными зависимостями (для интеграционных тестов)"""
    from api.controllers.user_controller import UserController
    
    async def provide_real_user_service() -> AsyncMock:
        return user_service
    
    app = Litestar(
        route_handlers=[UserController],
        dependencies={
            "user_service": Provide(provide_real_user_service, sync_to_thread=False),
        }
    )
    return app

@pytest.fixture
def real_test_client(real_test_app):
    """TestClient с реальными зависимостями"""
    from litestar.testing import TestClient
    return TestClient(app=real_test_app)