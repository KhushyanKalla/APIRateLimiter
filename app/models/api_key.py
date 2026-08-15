from app.core.database import Base
from sqlalchemy import String, func, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column
import datetime
import uuid

class ApiKey(Base):
    __tablename__ = "api_key_details"
    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    api_id : Mapped[int] = mapped_column(ForeignKey("api_details.id", ondelete="CASCADE"))
    is_active: Mapped[bool] = mapped_column(default=True)
    key_value: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    last_used_At :Mapped[datetime.datetime | None] = mapped_column(nullable= True)