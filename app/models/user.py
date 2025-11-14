from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID  # UUID тип для PostgreSQL
import uuid  # Генерация UUID
from app.database.database import Base  # Базовый класс для моделей
from datetime import datetime  # Для временных меток

class User(Base):
    __tablename__ = "users"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique = True,
        nullable=False
    )
    
    email = Column(
        String(255),
        unique= True,
        index=True,
        nullable=False
    )
    
    hashed_password = Column(
        String(255),
        nullable=False
    )
    
    full_name = Column(
        String(100),
        nullable=True
    )
    
    timezone = Column(
        String(50),
        default="UTC"
    )
    
    created_at = Column(
        DateTime,
        default=datetime.now
    )
    
    is_active = Column(
        Boolean,
        default=True
    )