from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete

from schemas.user_schemas import UserPostSchema, UserPatchSchema
from models.user_model import User


class UserRepository:
    def __init__(self, session: Session):
        self.__session = session
    
    def create(self, user_dto: UserPostSchema) -> User | None:
        query = insert(User).values(
            full_name=user_dto.full_name,
            email=user_dto.email,
            password=user_dto.password,
            problem_type=user_dto.problem_type
        ).returning(User)
        result = self.__session.execute(query)
        self.__session.commit()
        return result.scalar_one_or_none()

    def get_all(self) -> list[User]:
        query = select(User)
        result = self.__session.execute(query)
        return list(result.scalars().all())

    def patch(self, user_id: int, user_dto: UserPatchSchema) -> User | None:
        update_user = user_dto.model_dump(exclude_unset=True)
        query = update(User).where(User.id == user_id).values(**update_user).returning(User)
        result = self.__session.execute(query)
        self.__session.commit()
        return result.scalar_one_or_none()

    def delete(self, user_id: int) -> bool:
        query =delete(User).where(User.id == user_id).returning(User)
        result =self.__session.execute(query)
        self.__session.commit()
        return bool(result)
