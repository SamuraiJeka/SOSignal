from datetime import datetime, time, date, timedelta
from datetime import time, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func

from models import Stuff, Group, Order
from exceptions.stuff_exceptions import StuffNotFound


class StuffReposiotory:
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def get_stuff(self, current_time: time, order_date: date) -> list[int]:
        current_datetime = datetime.combine(order_date, current_time)
        one_hour_earlier = (current_datetime - timedelta(hours=1)).time()

        last_order_subq = (
            select(
                Group.stuff_id,
                Order.finish_time,
                func.max(Order.finish_time).over(partition_by=Group.stuff_id).label("max_finish")
            )
            .join(Order, Group.order_id == Order.id)
            .where(Order.order_date == order_date)
            .alias("last_order")
        )
        valid_last_order_subq = (
            select(last_order_subq.c.stuff_id)
            .select_from(last_order_subq)
            .where(
                last_order_subq.c.finish_time == last_order_subq.c.max_finish,
                last_order_subq.c.finish_time <= one_hour_earlier
            )
            .alias("valid_last_order")
        )

        query = (
            select(Stuff.id)
            .outerjoin(
                valid_last_order_subq, 
                Stuff.id == valid_last_order_subq.c.stuff_id
            )
            .outerjoin(Group, Stuff.id == Group.stuff_id)
            .where(
                or_(
                    valid_last_order_subq.c.stuff_id.is_not(None),
                    Group.id.is_(None)
                )
            )
            .distinct()
        )
        result = await self.__session.execute(query)
        stuff_list = list(result.scalars().all())
        if not stuff_list:
            raise StuffNotFound
        return stuff_list
