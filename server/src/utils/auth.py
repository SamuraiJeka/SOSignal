import jwt
from datetime import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.settings import settings
from core.database import get_session
from services.user_servise import UserService
from exceptions.auth_exceptions import TokenException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload["type"] != "access":
            raise TokenException("Неверный тип токена")
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise TokenException("Токен просрочен")
        
        email = payload["email"]
        async with get_session() as session:
            return await UserService(session).get_by_email(email)

    except jwt.PyJWKError:
        raise TokenException("Не удалось подтвердить учетные данные")