from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token

def register_user(user_data: UserCreate, db: Session) -> Token:
    existing = db.query(User).filter(User.email == user_data.email).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token({"sub": str(new_user.id)})
    
    return Token(access_token=token)

def authenticate_user(user_data: UserCreate, db: Session) -> Token:
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": str(user.id), "user_id": str(user.id)})
    
    return Token(access_token=token)