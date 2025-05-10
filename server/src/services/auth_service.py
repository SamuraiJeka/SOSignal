import jwt
import bcrypt
import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import settings
from repositories.user_repository import UserRepository
from exceptions.user_excptions import InvalidPassword
from schemas.user_schemas import (
    UserLoginSchema,
    UserPostSchema,
    UserSchema,
    TokenSchema
)


class AuthService:
    def __init__(self, session: AsyncSession):
        self.__user_repository = UserRepository(session)

    async def registration(self, user_dto: UserPostSchema) -> UserSchema:
        user_dto.password = await self.generate_password_hash(user_dto.password)
        user = await self.__user_repository.create(user_dto)
        return UserSchema.model_validate(user, from_attributes=True)
    
    async def login(self, user_dto: UserLoginSchema) -> TokenSchema:
        if not await self.check_password(user_dto):
            raise InvalidPassword
        tokens = await self.generate_tokens(user_dto.email)
        return TokenSchema(**tokens)

    async def check_password(self, user_dto: UserLoginSchema) -> bool:
        user = await self.__user_repository.get_by_email(user_dto.email)
        return bcrypt.checkpw(user.password.encode(), user_dto.password.encode())
    
    @staticmethod
    async def generate_password_hash( password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    @staticmethod
    async def generate_tokens(email: str) -> dict[str, str]:
        access_token_expires = datetime.timedelta(minutes=15)
        refresh_token_expires = datetime.timedelta(days=7)

        access_token_payload = {
            "email": email,
            "exp": datetime.datetime.now() + access_token_expires,
            "iat": datetime.datetime.now(),
            "type": "access"
        }
        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, settings.ALGORITHM)

        refresh_token_payload = {
            "email": email,
            "exp": datetime.datetime.now() + refresh_token_expires,
            "iat": datetime.datetime.now(),
            "type": "refresh"
        }
        refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, settings.ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
