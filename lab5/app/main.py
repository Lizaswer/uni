import os
from typing import AsyncGenerator

from api.controllers.user_controller import UserController
from api.models.user import Base
from api.repositories.user_repository import UserRepository
from api.services.user_service import UserService
from litestar import Litestar
from litestar.di import Provide
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)


def get_database_url() -> str:
    """Получаем URL базы данных с учетом окружения"""
    if os.getenv("TESTING"):
        return "sqlite+aiosqlite:///:memory:"
    return os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://litestar_user:litestar_password@localhost:5432/litestar_lab3"
    )

# Настройка базы данных
DATABASE_URL = get_database_url()

# Создание движка SQLAlchemy
engine = create_async_engine(
    DATABASE_URL,
    echo=bool(os.getenv("SQL_ECHO", False)),
    pool_pre_ping=True,
    pool_recycle=300,
)

# Фабрика сессий
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Провайдер сессии базы данных"""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    """Провайдер репозитория пользователей"""
    return UserRepository()

async def provide_user_service(
    user_repository: UserRepository, 
    db_session: AsyncSession
) -> UserService:
    """Провайдер сервиса пользователей"""
    return UserService(user_repository, db_session)

async def on_startup():
    """Создание таблиц при запуске приложения"""
    if not os.getenv("TESTING"):  # Не создаем таблицы в тестовом режиме
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully")

async def on_shutdown():
    """Закрытие соединений при завершении приложения"""
    await engine.dispose()
    if not os.getenv("TESTING"):
        print("✅ Database connections closed")

# Создаем приложение
def create_app() -> Litestar:
    return Litestar(
        route_handlers=[UserController],
        dependencies={
            "db_session": Provide(provide_db_session),
            "user_repository": Provide(provide_user_repository),
            "user_service": Provide(provide_user_service),
        },
        on_startup=[on_startup] if not os.getenv("TESTING") else None,
        on_shutdown=[on_shutdown] if not os.getenv("TESTING") else None
    )

# Глобальная переменная app для импорта
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )