from app.core.database import Base
from sqlalchemy import String, Enum, func

from sqlalchemy.orm import Mapped, mapped_column
import datetime
import enum


class UserTier(str, enum.Enum):
    PREMIUM = "Premium"
    FREE = "Free"

class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(200), unique=True)
    password_hash : Mapped[str] = mapped_column(String(200))
    is_active : Mapped[bool] = mapped_column(default=True)
    tier : Mapped[UserTier] = mapped_column(Enum(UserTier), default=UserTier.FREE)
    created_at : Mapped[datetime.datetime] = mapped_column(server_default=func.now())

#id (Integer, PK, autoincrement), name (String), email (String, unique), password_hash (String), is_active (Bool), 
# tier (Enum), created_at (DateTime, default=now)