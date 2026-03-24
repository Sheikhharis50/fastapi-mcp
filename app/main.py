from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import Base, engine
from .middlewares.timer import request_timer_middleware
from .schemas.api import ApiResponse
from .routers.api import router as user_router
from .routers.mcp import router as mcp_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="FastAPI + MCP Demo", lifespan=lifespan)


# Middleware
app.middleware("http")(request_timer_middleware)


# Routers
app.include_router(user_router)
app.include_router(mcp_router)


@app.get("/health")
async def health():
    return ApiResponse(message="OK")
