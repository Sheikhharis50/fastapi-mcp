from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.api import ApiResponse
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user import create_user, delete_user, get_user, get_users, update_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=ApiResponse)
async def create(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await create_user(db, user.name, user.email)
    return ApiResponse(
        message="User created successfully",
        data=UserResponse.model_validate(user),
    )


@router.get("/", response_model=ApiResponse)
async def list_users(db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    return ApiResponse(
        message="Users fetched successfully",
        data=[UserResponse.model_validate(u) for u in users],
    )


@router.get("/{user_id}", response_model=ApiResponse)
async def get(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    return ApiResponse(
        message="User fetched successfully",
        data=UserResponse.model_validate(user),
    )


@router.put("/{user_id}", response_model=ApiResponse)
async def update(user_id: int, body: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await update_user(db, user_id, body.name, body.email)
    return ApiResponse(
        message="User updated successfully",
        data=UserResponse.model_validate(user),
    )


@router.delete("/{user_id}", response_model=ApiResponse)
async def delete(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await delete_user(db, user_id)
    return ApiResponse(
        message="User deleted successfully",
        data=UserResponse.model_validate(user),
    )
