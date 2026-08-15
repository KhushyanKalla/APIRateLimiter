from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_token
from app.crud.user import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):

    verified_token = verify_token(token)

    if not verified_token:
        raise HTTPException(401, "Invalid or expired token")

    user = await get_user_by_email(db,verified_token)

    if not user:
        raise HTTPException(401, "No User")

    return user