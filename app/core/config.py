"""
Модуль конфигурации приложения.
Исправленная версия для работы со строкой ALLOWED_ORIGINS.
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Класс настроек приложения."""
    
    # Настройки базы данных
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost/habittracker"
    
    # Настройки JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Настройки CORS - как строка (именно так как в вашем .env)
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    def get_allowed_origins(self) -> List[str]:
        """Преобразуем строку ALLOWED_ORIGINS в список для CORS."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"

settings = Settings()