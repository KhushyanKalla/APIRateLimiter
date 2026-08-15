from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.security import password_hash

async def create_user(db : AsyncSession, user_date : UserCreate)->User:
    new_data = User(
        name = user_date.name,
        email = user_date.email,
        password_hash=password_hash(user_date.password)
    )
    db.add(new_data)
    await db.commit()
    await db.refresh(new_data)
    return new_data

async def get_user_by_email(db :AsyncSession , email : str)-> User |None:
    user = await db.execute(select(User).where(User.email == email))
    return user.scalar_one_or_none()