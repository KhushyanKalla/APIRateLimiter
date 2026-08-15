# id (BigInt, PK, autoincrement), api_key_id (FK→APIKey), timestamp (DateTime, default=now)
from app.core.database import Base
from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey, func
import datetime

class Reqlog(Base):
    __tablename__ = "request_log_table"
    
    id : Mapped[int] = mapped_column(BigInteger,primary_key=True)
    api_key_id : Mapped[int] = mapped_column(ForeignKey("api_key_details.id", ondelete="CASCADE"))
    timestamp : Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    
    