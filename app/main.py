from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import auth, api as api_router, api_key
from app.core.database import Base, engine
from app.models import user  # zaroori hai, warna table register hi nahi hogi
from app.models import api as api_model
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.middleware.rate_limiter import RateLimiterMiddleware




@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


# UI integration: Mount static files for frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/", include_in_schema=False)
async def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

app.include_router(auth.router)
app.include_router(api_router.router)
app.include_router(api_key.router)

app.add_middleware(RateLimiterMiddleware)