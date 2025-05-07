from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, exists

from schemas.user_schemas import UserPostSchema, UserPatchSchema
from models import User
from exceptions.user_excptions import (
    UserNotFound,
    UserAlreadyExist,
    UserListIsEmpty
)


class UserRepository:
    def __init__(self, session: Session):
        self.__session = session
    
    def create(self, user_dto: UserPostSchema) -> User | None:
        if self.is_exists(email=user_dto.email):
            raise UserAlreadyExist(user_dto.email)
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
        user_list = list(result.scalars().all())
        if not user_list:
            raise UserListIsEmpty
        return user_list

    def update(self, user_id: int, user_dto: UserPatchSchema) -> User | None:
        update_user = user_dto.model_dump(exclude_unset=True)
        query = update(User).where(User.id == user_id).values(**update_user).returning(User)
        result = self.__session.execute(query)
        self.__session.commit()
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFound
        return user

    def delete(self, user_id: int) -> bool:
        query = delete(User).where(User.id == user_id).returning(User)
        result = self.__session.execute(query)
        if result.scalar() is None:
            raise UserNotFound
        self.__session.commit()
        return bool(result)

    def is_exists(
        self,
        email: str | None = None,
        id: int | None = None
    ) -> bool | None:
        if id is not None:
            query = select(exists().where(User.id == id))
        elif email is not None:
            query = select(exists().where(User.email == email))
        else:
            raise ValueError("Incorrect function overload")
        result = self.__session.execute(query)
        return result.scalar()
