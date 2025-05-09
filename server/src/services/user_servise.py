from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user_repository import UserRepository
from schemas.user_schemas import UserPostSchema, UserSchema, UserPatchSchema


class UserService:
    def __init__(self, session: AsyncSession):
        self.__reposiotory = UserRepository(session)

    async def create(self, user_dto: UserPostSchema) -> UserSchema:
        user = await self.__reposiotory.create(user_dto)
        return UserSchema.model_validate(user, from_attributes=True)

    async def get_all(self) -> list[UserSchema]:
        user_list = await self.__reposiotory.get_all()
        return [UserSchema.model_validate(user, from_attributes=True) for user in user_list]

    async def update(self, user_id: int, user_dto: UserPatchSchema) -> UserSchema:
        user = await self.__reposiotory.update(user_id, user_dto)
        return UserSchema.model_validate(user, from_attributes=True)

    async def delete(self, user_id: int) -> bool:
        result = await self.__reposiotory.delete(user_id)
        return result
