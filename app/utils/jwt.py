from datetime import datetime, timedelta, timezone

from jose import jwt
from app.core.config import settings

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
def create_access_token(data: dict):
    to_encode = data.copy()
    
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)