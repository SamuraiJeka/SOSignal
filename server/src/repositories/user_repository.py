from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, exists, and_

from schemas.order_schemas import OrderPostSchema
from schemas.user_schemas import (
    UserPostSchema,
    UserPatchSchema,
)
from models import User, Order
from exceptions.user_excptions import (
    UserNotFound,
    UserAlreadyExist,
    UserListIsEmpty
)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def create(self, user_dto: UserPostSchema) -> User | None:
        if await self.is_exists(email=user_dto.email):
            raise UserAlreadyExist(user_dto.email)
        query = insert(User).values(
            full_name=user_dto.full_name,
            email=user_dto.email,
            password=user_dto.password,
            problem_type=user_dto.problem_type
        ).returning(User)
        result = await self.__session.execute(query)
        await self.__session.commit()
        user = result.scalar_one_or_none()
        await self.__session.refresh(user)
        return user

    async def get_all(self) -> list[User]:
        query = select(User)
        result = await self.__session.execute(query)
        user_list = list(result.scalars().all())
        if not user_list:
            raise UserListIsEmpty
        return user_list
    
    async def get_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.__session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFound
        return user
    
    async def get_problem_by_id(self, user_id: int) -> str:
        query = select(User).where(User.id == user_id)
        result = await self.__session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFound
        return user.problem_type.name

    async def update(self, user_id: int, user_dto: UserPatchSchema) -> User | None:
        update_user = user_dto.model_dump(exclude_unset=True)
        query = update(User).where(User.id == user_id).values(**update_user).returning(User)
        result = await self.__session.execute(query)
        await self.__session.commit()
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFound
        await self.__session.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        query = delete(User).where(User.id == user_id).returning(User)
        result = await self.__session.execute(query)
        if result.scalar() is None:
            raise UserNotFound
        await self.__session.commit()
        return bool(result)

    async def is_exists(
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
        result = await self.__session.execute(query)
        return result.scalar()

    async def repetition_check(self, user_id: int, order_dto: OrderPostSchema) -> bool:
        query = (
            select(Order)
            .where(
                and_(
                    Order.start_time == order_dto.start_time,
                    Order.order_date == order_dto.order_date,
                    Order.user_id == user_id
                )
            )
        )
        result = await self.__session.execute(query)
        if result.scalar() is None:
            return False
        return True
