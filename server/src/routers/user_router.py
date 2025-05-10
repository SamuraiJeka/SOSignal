from fastapi import APIRouter, HTTPException, Depends

from core.database import get_session
from schemas.user_schemas import UserPostSchema, UserSchema, UserPatchSchema
from services.user_servise import UserService
from utils.auth import get_current_user
from exceptions.user_excptions import (
    UserNotFound,
    UserAlreadyExist,
    UserListIsEmpty
)


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", status_code=201)
async def post_user(
    user_dto: UserPostSchema, 
    current_user: UserSchema = Depends(get_current_user)
) -> UserSchema:
    try:
        async with get_session() as session:
            return await UserService(session).create(user_dto=user_dto)
    except UserAlreadyExist as exc:
        raise HTTPException(status_code=exc.status, detail=exc.msg)


@router.get("/", status_code=200)
async def get_all_users(
    current_user: UserSchema = Depends(get_current_user)
) -> list[UserSchema]:
    try:
        async with get_session() as session:
            return await UserService(session).get_all()
    except UserListIsEmpty as exc:
        raise HTTPException(status_code=exc.status, detail=exc.msg)


@router.patch("/{id}", status_code=200)
async def patch_user(
    id: int,
    user_dto: UserPatchSchema,
    current_user: UserSchema = Depends(get_current_user)
) -> UserSchema:
    try:
        async with get_session() as session:
            return await UserService(session).update(id, user_dto)
    except UserNotFound as exc:
        raise HTTPException(status_code=exc.status, detail=exc.msg)


@router.delete("/{id}", status_code=200)
async def delete_user(
    id: int,
    current_user: UserSchema = Depends(get_current_user)
) -> bool:
    try:
        async with get_session() as session:
            return await UserService(session).delete(id)
    except UserNotFound as exc:
        raise HTTPException(status_code=exc.status, detail=exc.msg)
