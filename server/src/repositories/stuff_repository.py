from datetime import time, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, join, text

from models import Stuff, Group, Order
from exceptions.stuff_exceptions import StuffNotFound


class StuffReposiotory:
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def get_stuff(self, current_time: time, order_date: date) -> list[Stuff]:
        query = (
            select(Stuff)
            .join(Group, Stuff.id == Group.stuff_id)
            .join(Order, Group.order_id == Order.id)
            .where(
                Order.order_date == order_date,
                Order.finish_time < current_time - text("INTERVAL '1 hour'")
            )
            .distinct()
        )
        result = await self.__session.execute(query)
        stuff_list = list(result.scalars().all())
        if not stuff_list:
            raise StuffNotFound
        return stuff_list
