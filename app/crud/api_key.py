import hashlib
import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.api_key import ApiKey

def hash_key (raw_key : str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()

async def create_api_key(db: AsyncSession, api_id: int) -> tuple[ApiKey, str]:
    raw_key = secrets.token_urlsafe(32)
    hashed = hash_key(raw_key)
    
    new_key = ApiKey(api_id=api_id, key_value=hashed)
    db.add(new_key)
    await db.commit()
    await db.refresh(new_key)
    
    return new_key, raw_key