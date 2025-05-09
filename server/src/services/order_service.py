from sqlalchemy.ext.asyncio import AsyncSession

from repositories.order_repository import OrderRepository
from repositories.user_repository import UserRepository
from schemas.order_schemas import OrderPostSchema, OrderSchema
from exceptions.user_excptions import UserNotFound


#TODO: Интегрировать сервис группы. Написать логику распределения персонала по заявкам.
class OrderService:
    async def __init__(self, session: AsyncSession):
        self.__repository = OrderRepository(session)
        self.__user_repository = UserRepository(session)
    
    async def create(self, order_dto: OrderPostSchema) -> OrderSchema:
        if not await self.__user_repository.is_exists(id=order_dto.user_id):
            raise UserNotFound
        order = await self.__repository.create(order_dto)
        return OrderSchema.model_validate(order, from_attributes=True)

    async def get_by_user_id(self, user_id: int) -> list[OrderSchema]:
        if not await self.__user_repository.is_exists(id=user_id):
            raise UserNotFound
        order_list = await self.__repository.get_by_user_id(user_id)
        return [
            OrderSchema.model_validate(order, from_attributes=True) for order in order_list
        ]

    async def delete(self, order_id: int) -> bool | None:
        result = await self.__repository.delete(order_id)
        return result
