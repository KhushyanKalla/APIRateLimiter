from app.schemas.api import ApiCreate, ApiResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud.api import create_api, get_api_by_user
from app.models.user import User
from app.dependencies.auth import get_current_user


router = APIRouter(prefix="/apis", tags=["Api"])

@router.post("/", response_model=ApiResponse)
async def apis (api_data : ApiCreate, db : AsyncSession = Depends(get_db), user : User = Depends(get_current_user)):
    return await create_api(db, api_data, user.id)

@router.get("/", response_model=list[ApiResponse])
async def list_api(db : AsyncSession = Depends(get_db), user : User = Depends(get_current_user)):
    return await get_api_by_user(db, user.id)
    