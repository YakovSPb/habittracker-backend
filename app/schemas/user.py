from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserLogin):
    full_name: str 
    
class UserOut(BaseModel):
    id: UUID
    full_name: str | None
    email: EmailStr
    timezone: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
        