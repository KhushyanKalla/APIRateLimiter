from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from sqlalchemy import Enum
from datetime import datetime


class ReqResponse(BaseModel):
    id :int 
    api_key_id : UUID
    timestamp : datetime
       
    model_config = {"from_attributes": True}
