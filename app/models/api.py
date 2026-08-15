from app.core.database import Base
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
import datetime

class Api (Base):
    __tablename__ = "api_details"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name : Mapped[str] = mapped_column(String(255))
    created_at : Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    