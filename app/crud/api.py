from sqlalchemy.ext.asyncio import AsyncSession
from app.models.api import Api
from app.schemas.api import ApiCreate
from sqlalchemy import select


async def create_api (db: AsyncSession, api_data : ApiCreate, user_id : int)->Api:
    new = Api(
        name = api_data.name,
        user_id = user_id
    )
    db.add(new)
    await db.commit()
    await db.refresh(new)
    return new

async def get_api_by_id(db : AsyncSession, id : int )->Api | None:
    search = await db.execute(select(Api).where(Api.id == id))
    return search.scalar_one_or_none()

async def get_api_by_user(db: AsyncSession, user_id: int) -> list[Api]:
    result = await db.execute(select(Api).where(Api.user_id == user_id))
    return result.scalars().all()