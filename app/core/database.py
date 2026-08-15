from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

engine = create_async_engine(settings.DATABASE_URL, echo = True)
AsyncSessionBank = async_sessionmaker(autoflush = True, expire_on_commit= False, bind=engine)

class Base(DeclarativeBase):
    pass


async def get_db()-> AsyncGenerator[AsyncSession,None]:
    async with AsyncSessionBank() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()