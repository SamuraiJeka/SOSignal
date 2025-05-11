from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete

from models import Order
from schemas.order_schemas import OrderPostSchema
from exceptions.order_exceptions import OrderNotFound


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def create(self, user_id: int, order_dto: OrderPostSchema) -> Order | None:
        query = insert(Order).values(
            user_id=user_id,
            baggage=order_dto.baggage,
            order_date=order_dto.order_date,
            start_time=order_dto.start_time,
            finish_time=order_dto.finish_time
        ).returning(Order)
        result = await self.__session.execute(query)
        await self.__session.commit()
        order = result.scalar_one_or_none()
        self.__session.refresh(order)
        return order

    async def get_by_user_id(self, user_id: int) -> list[Order]:
        query = select(Order).where(Order.user_id == user_id)
        result = await self.__session.execute(query)
        return list(result.scalars().all())
    
    async def delete(self, order_id: int) -> bool | None:
        query = delete(Order).where(Order.id == order_id)
        result = await self.__session.execute(query)
        if result.scalar() is None:
            raise OrderNotFound
        await self.__session.commit()
        return bool(result)
