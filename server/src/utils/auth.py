import jwt
from datetime import datetime
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.settings import settings
from core.database import get_session
from services.user_servise import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload["type"] != "access":
            raise credentials_exception
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise credentials_exception
        
        email = payload["email"]
        async with get_session() as session:
            return await UserService(session).get_by_email(email)

    except jwt.PyJWKError:
        raise credentials_exception
