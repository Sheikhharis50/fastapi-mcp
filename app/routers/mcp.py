from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import create_user, delete_user, get_user, get_users, update_user

router = APIRouter(prefix="/mcp", tags=["MCP"])


class UserIdInput(BaseModel):
    user_id: int = Field(..., gt=0)


class UserUpdateInput(UserUpdate):
    user_id: int = Field(..., gt=0)


class MCPRequest(BaseModel):
    tool: str
    input: dict = {}


TOOL_SCHEMAS: dict[str, type[BaseModel] | None] = {
    "create_user": UserCreate,
    "get_user": UserIdInput,
    "list_users": None,
    "update_user": UserUpdateInput,
    "delete_user": UserIdInput,
}


@router.post("/invoke")
async def invoke(req: MCPRequest, db: AsyncSession = Depends(get_db)):
    if req.tool not in TOOL_SCHEMAS:
        raise HTTPException(status_code=400, detail=f"Unknown tool: {req.tool}")

    schema = TOOL_SCHEMAS[req.tool]
    try:
        data = schema(**req.input) if schema else None
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

    if req.tool == "create_user":
        return await create_user(db, data.name, data.email)

    if req.tool == "get_user":
        return await get_user(db, data.user_id)

    if req.tool == "list_users":
        return await get_users(db)

    if req.tool == "update_user":
        return await update_user(db, data.user_id, data.name, data.email)

    if req.tool == "delete_user":
        return await delete_user(db, data.user_id)
