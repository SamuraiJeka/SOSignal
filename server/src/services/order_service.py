from sqlalchemy.ext.asyncio import AsyncSession

from repositories.order_repository import OrderRepository
from repositories.user_repository import UserRepository
from repositories.group_repository import GroupReposiotory
from repositories.stuff_repository import StuffReposiotory

from schemas.order_schemas import OrderPostSchema, OrderSchema
from schemas.stuff_schemas import StuffSchema

from exceptions.user_excptions import UserNotFound
from exceptions.stuff_exceptions import Understaffed
from exceptions.order_exceptions import TimeConflict


class OrderService:
    def __init__(self, session: AsyncSession):
        self.__order_repository = OrderRepository(session)
        self.__user_repository = UserRepository(session)
        self.__stuff_repository = StuffReposiotory(session)
        self.__group_repository = GroupReposiotory(session)
    
    async def create(self, user_id: int, order_dto: OrderPostSchema) -> OrderSchema:
        if not await self.__user_repository.is_exists(id=user_id):
            raise UserNotFound
        if await self.__user_repository.repetition_check(user_id, order_dto.start_time) is not None:
            raise TimeConflict
        stuff_list = await self.__stuff_repository.get_stuff(
            order_dto.start_time,
            order_dto.order_date
        )
        stuff_count = await self.get_stuff_count(
            user_id,
            order_dto.baggage
        )
        print(f"---------------{stuff_list}")
        print(f"======={stuff_count}")
        if len(stuff_list) < stuff_count:
            raise Understaffed
        order = await self.__order_repository.create(user_id, order_dto)
        await self.__group_repository.create(stuff_list[:stuff_count], order.id)
        return OrderSchema.model_validate(order, from_attributes=True)

    async def get_by_user_id(self, user_id: int) -> list[OrderSchema]:
        if not await self.__user_repository.is_exists(id=user_id):
            raise UserNotFound
        order_list = await self.__order_repository.get_by_user_id(user_id)
        return [
            OrderSchema.model_validate(order, from_attributes=True)
            for order in order_list
        ]
    
    async def get_stuff_by_id(self, order_id: int) -> list[StuffSchema]:
        stuff_list = await self.__stuff_repository.get_stuff_by_order_id(
            order_id
        )
        return [
            StuffSchema.model_validate(stuff, from_attributes=True)
            for stuff in stuff_list
        ]

    async def delete(self, order_id: int) -> bool | None:
        result = await self.__order_repository.delete(order_id)
        return result

    async def get_stuff_count(self, user_id: int, baggage: bool) -> int:
        problem_type = await self.__user_repository.get_problem_by_id(user_id)
        baggage_idx = 2 if baggage else 1
        problem_idx = 1 if problem_type == "BLINDNESS" else 1.5
        return round(problem_idx * baggage_idx)
