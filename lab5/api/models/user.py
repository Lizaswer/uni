from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base  # Используем правильный импорт
from sqlalchemy.sql import func

Base = declarative_base()  # Теперь правильный импорт

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# Pydantic модели
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)