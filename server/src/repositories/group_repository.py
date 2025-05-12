from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from models import Group


class GroupReposiotory:
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def create(self, stuff_list: list[int], order_id: int) -> None:
        values = [{"stuff_id": stuff_id, "order_id": order_id} for stuff_id in stuff_list]
        query = insert(Group).values(values)
        await self.__session.execute(query)
        await self.__session.commit()
