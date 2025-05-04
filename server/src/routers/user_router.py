from fastapi import APIRouter

from core.database import get_session
from schemas.user_schemas import UserPostSchema, UserSchema, UserPatchSchema
from services.user_servise import UserService


router = APIRouter(prefix="/user")


@router.post("/", status_code=200)
def post_user(user_dto: UserPostSchema) -> UserSchema:
    with get_session() as session:
        return UserService(session).create(user_dto=user_dto)


@router.get("/", status_code=200)
def get_all_users() -> list[UserSchema]:
    with get_session() as session:
        return UserService(session).get_all()
    

@router.patch("/{id}", status_code=200)
def patch_user(id: int, user_dto: UserPatchSchema) -> UserSchema:
    with get_session() as session:
        return UserService(session).patch(id, user_dto)


@router.delete("/{id}", status_code=200)
def delete_user(id: int) -> bool:
    with get_session() as session:
        return UserService(session).delete(id)