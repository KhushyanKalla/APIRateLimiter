import hashlib
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.redis import redis_client
from app.core.database import AsyncSessionBank
from sqlalchemy import select
from app.models.api_key import ApiKey
import asyncio
from app.models.request_log import Reqlog

async def log_request(api_key_id):
    async with AsyncSessionBank() as db:
        new_log = Reqlog(api_key_id=api_key_id)
        db.add(new_log)
        await db.commit()
FREE_TIER_LIMIT = 1000
WINDOW_SECONDS = 30 * 24 * 60 * 60  # 30 din

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key_header = request.headers.get("X-API-Key")
        
        if not api_key_header:
            return await call_next(request)  # koi key nahi -> normal routes ke liye pass through
        
        hashed = hashlib.sha256(api_key_header.encode()).hexdigest()
        
        async with AsyncSessionBank() as db:
            result = await db.execute(select(ApiKey).where(ApiKey.key_value == hashed))
            key_obj = result.scalar_one_or_none()
        
        if not key_obj or not key_obj.is_active:
            return JSONResponse(status_code=401, content={"detail": "Invalid API key"})
        
        redis_key = f"rate_limit:{key_obj.id}"
        count = await redis_client.incr(redis_key)
        
        if count == 1:
            await redis_client.expire(redis_key, WINDOW_SECONDS)
        
        if count > FREE_TIER_LIMIT:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        
        response = await call_next(request)
        asyncio.create_task(log_request(key_obj.id))
        return response