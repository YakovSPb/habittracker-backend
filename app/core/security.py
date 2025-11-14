"""
Модуль безопасности.
Содержит функции для работы с паролями и JWT токенами.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Создаем контекст для хеширования паролей с использованием bcrypt
# bcrypt - надежный алгоритм хеширования, специально разработанный для паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли plain_password хешу hashed_password.
    
    Args:
        plain_password: Пароль в чистом виде
        hashed_password: Хешированный пароль из базы данных
    
    Returns:
        bool: True если пароли совпадают, False если нет
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Создает bcrypt хеш пароля.
    
    Args:
        password: Пароль в чистом виде
    
    Returns:
        str: Хешированный пароль
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создает JWT токен доступа.
    
    Args:
        data: Данные для кодирования в токене (обычно user_id)
        expires_delta: Время жизни токена, если не указано - используется настройка по умолчанию
    
    Returns:
        str: Закодированный JWT токен
    """
    # Копируем данные чтобы не изменять оригинал
    to_encode = data.copy()
    
    # Устанавливаем время истечения токена
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Добавляем время истечения в данные токена
    to_encode.update({"exp": expire})
    
    # Кодируем данные в JWT токен
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt