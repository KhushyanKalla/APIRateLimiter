from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.models.request_log import Reqlog
from app.models.api_key import ApiKey
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/key/{api_key_id}/count")
async def get_request_count(api_key_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(
        select(func.count(Reqlog.id)).where(Reqlog.api_key_id == api_key_id)
    )
    total = result.scalar()
    return {"api_key_id": api_key_id, "total_requests": total}