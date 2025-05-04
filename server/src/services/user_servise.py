from sqlalchemy.orm import Session

from repositories.user_repository import UserRepository
from schemas.user_schemas import UserPostSchema, UserSchema, UserPatchSchema

class UserService:
    def __init__(self, session: Session):
        self.__reposiotory = UserRepository(session)

    def create(self, user_dto: UserPostSchema) -> UserSchema:
        user = self.__reposiotory.create(user_dto)
        return UserSchema().model_validate(user, from_attributes=True)

    def get_all(self) -> list[UserSchema]:
        user_list = self.__reposiotory.get_all()
        return [UserSchema.model_validate(user, from_attributes=True) for user in user_list]
    
    def patch(self, user_id: int, user_dto: UserPatchSchema) -> UserSchema:
        user = self.__reposiotory.patch(user_id, user_dto)
        return UserSchema.model_validate(user, from_attributes=True)
    
    def delete(self, user_id: int) -> bool:
        result = self.__reposiotory.delete(user_id)
        return result
