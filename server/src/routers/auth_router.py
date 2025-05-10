from fastapi import APIRouter, HTTPException

from core.database import get_session
from schemas.user_schemas import UserPostSchema, UserLoginSchema, UserSchema, TokenSchema
from services.auth_service import AuthService
from exceptions.user_excptions import UserAlreadyExist, InvalidPassword, UserNotFound



router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registration", status_code=201)
async def registration(user_dto: UserPostSchema) -> UserSchema:
    try:
        async with get_session() as session:
            return await AuthService(session).registration(user_dto)
    except UserAlreadyExist as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)


@router.post("/login")
async def login(user_dto: UserLoginSchema) -> TokenSchema:
    try:
        async with get_session() as session:
            return await AuthService(session).login(user_dto)
    except InvalidPassword as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)
    except UserNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)
