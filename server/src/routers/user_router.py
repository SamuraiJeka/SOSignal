from fastapi import APIRouter, HTTPException

from core.database import get_session
from schemas.user_schemas import UserPostSchema, UserSchema, UserPatchSchema
from services.user_servise import UserService
from exceptions.user_excptions import (
    UserNotFound,
    UserAlreadyExist,
    UserListIsEmpty
)


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", status_code=200)
def post_user(user_dto: UserPostSchema) -> UserSchema:
    try:
        with get_session() as session:
            return UserService(session).create(user_dto=user_dto)
    except UserAlreadyExist as exc:
        raise HTTPException(status_code=exc.status, detail=exc.msg)


@router.get("/", status_code=200)
def get_all_users() -> list[UserSchema]:
    try:
        with get_session() as session:
            return UserService(session).get_all()
    except UserListIsEmpty as exc:
        raise HTTPException(status_code=exc.status, detail=exc.msg)
    

@router.patch("/{id}", status_code=200)
def patch_user(id: int, user_dto: UserPatchSchema) -> UserSchema:
    try:
        with get_session() as session:
            return UserService(session).update(id, user_dto)
    except UserNotFound as exc:
        raise HTTPException(status_code=exc.status, detail=exc.msg)


@router.delete("/{id}", status_code=200)
def delete_user(id: int) -> bool:
    try:
        with get_session() as session:
            return UserService(session).delete(id)
    except UserNotFound as exc:
        raise HTTPException(status_code=exc.status, detail=exc.msg)
