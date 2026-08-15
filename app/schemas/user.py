from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from sqlalchemy import Enum
from datetime import datetime
from app.models.user import UserTier

# id (Integer, PK, autoincrement), name (String), email (String, unique), password_hash (String), is_active (Bool), tier (Enum), created_at (DateTime, default=now)
class UserCreate(BaseModel):
    name : str = Field(..., min_length=3)
    email : EmailStr
    password: str = Field(..., min_length=4)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    tier: UserTier
    created_at: datetime
    model_config = {"from_attributes": True}
    
    
class UserLogin(BaseModel):
    email : EmailStr
    password : str = Field(..., min_length=4)