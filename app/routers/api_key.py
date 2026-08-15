from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud.api_key import create_api_key
from app.crud.api import get_api_by_id
from app.schemas.api_key import ApiKeyCreateResponse
from app.models.user import User
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/apis/{api_id}/keys", tags=["ApiKeys"])

@router.post("/", response_model=ApiKeyCreateResponse)
async def generate_key(api_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    is_exist = await get_api_by_id(db, api_id)
    if not is_exist:
        raise HTTPException(status_code=404, detail="API not found")
    if is_exist.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    key_obj, raw_key = await create_api_key(db, api_id)
    return {
        "id": key_obj.id,
        "api_id": key_obj.api_id,
        "raw_key": raw_key,
        "created_at": key_obj.created_at
    }