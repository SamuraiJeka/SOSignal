import jwt
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.settings import settings
from core.database import get_session
from services.user_servise import UserService
from schemas.user_schemas import UserSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    expired_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        if payload.get("type") != "access":
            raise credentials_exception
            
        email = payload.get("email")
        if not email:
            raise credentials_exception
            
        async with get_session() as session:
            return await UserService(session).get_by_email(email)
            
    except ExpiredSignatureError:
        raise expired_token_exception
    except PyJWTError:
        raise credentials_exception
