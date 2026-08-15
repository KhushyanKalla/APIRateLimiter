from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from sqlalchemy import Enum
from datetime import datetime



class ApiCreate(BaseModel):
    name : str = Field(..., min_length=3)
    
class ApiResponse(BaseModel):

    
    id: int
    user_id: int
    name: str
    created_at: datetime
    
    model_config = {"from_attributes": True}
