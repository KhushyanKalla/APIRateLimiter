from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from sqlalchemy import Enum
from datetime import datetime



class ApikeyCreate(BaseModel):
    raw_key: str
    id: UUID
    api_id: int
    created_at: datetime

class ApikeyResponse(BaseModel):
    id: UUID
    api_id: int
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]
    
    model_config = {"from_attributes": True}
    

class ApiKeyCreateResponse(BaseModel):
    id: UUID
    api_id: int
    raw_key: str
    created_at: datetime
