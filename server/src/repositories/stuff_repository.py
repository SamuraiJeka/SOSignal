from datetime import datetime, time, date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func, DateTime, String

from models import Stuff, Group, Order
from exceptions.stuff_exceptions import StuffNotFound


class StuffReposiotory:
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def get_stuff(self, current_time: time, order_date: date) -> list[int]:
        current_datetime = datetime.combine(order_date, current_time)
        one_hour_before = (current_datetime - timedelta(hours=1)).time()

        last_order_subq = (
        select(
            Group.stuff_id,
            Order.finish_time,
            Order.order_date,
            # Используем строковую конкатенацию даты и времени с последующим приведением к timestamp
            func.max(
                func.cast(
                    func.concat(
                        func.cast(Order.order_date, String),
                        ' ',
                        func.cast(Order.finish_time, String)
                    ),
                    DateTime
                )
            ).over(partition_by=Group.stuff_id).label("max_order_datetime")
        )
        .join(Order, Group.order_id == Order.id)
        .where(Order.order_date <= order_date)
        .alias("last_order")
    )

        valid_last_order_subq = (
            select(last_order_subq.c.stuff_id)
            .select_from(last_order_subq)
            .where(
                # Сравниваем через строковую конкатенацию
                func.cast(
                    func.concat(
                        func.cast(last_order_subq.c.order_date, String),
                        ' ',
                        func.cast(last_order_subq.c.finish_time, String)
                    ),
                    DateTime
                ) == last_order_subq.c.max_order_datetime,
                # Условия по времени
                or_(
                    last_order_subq.c.order_date < order_date,
                    and_(
                        last_order_subq.c.order_date == order_date,
                        last_order_subq.c.finish_time <= one_hour_before
                    )
                )
            )
            .alias("valid_last_order")
        )

        query = (
            select(Stuff.id)
            .outerjoin(valid_last_order_subq, Stuff.id == valid_last_order_subq.c.stuff_id)
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

    async def get_stuff_by_order_id(self, order_id: int) -> list[Stuff]:
        query = (
            select(Stuff)
            .join(Group, Group.stuff_id == Stuff.id)
            .where(Group.order_id == order_id)
        )
        result = await self.__session.execute(query)
        stuff_list = list(result.scalars().all())
        if not stuff_list:
            raise StuffNotFound
        return stuff_list
