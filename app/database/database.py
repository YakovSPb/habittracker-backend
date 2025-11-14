"""
Модуль работы с базой данных.
Содержит настройку подключения к PostgreSQL и создание сессий.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создаем движок базы данных - основной источник подключения к БД
# echo=True включает логирование SQL запросов (полезно для разработки)
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # В продакшене лучше установить False
)

# SessionLocal - фабрика для создания сессий базы данных
# autocommit=False - отключаем автоматический коммит (контролируем вручную)
# autoflush=False - отключаем автоматический flush (также контролируем вручную)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base - базовый класс для всех моделей SQLAlchemy
# Все модели будут наследоваться от этого класса
Base = declarative_base()

def get_db():
    """
    Dependency (зависимость) для получения сессии базы данных.
    FastAPI будет автоматически вызывать эту функцию при запросах.
    
    Yields:
        Session: Сессия базы данных
    
    Guarantees:
        Сессия будет закрыта даже при возникновении исключения
    """
    # Создаем новую сессию
    db = SessionLocal()
    try:
        # Отдаем сессию вызывающему коду (например, роутеру)
        yield db
    finally:
        # Всегда закрываем сессию, даже если произошла ошибка
        # Это важно для предотвращения утечек соединений
        db.close()