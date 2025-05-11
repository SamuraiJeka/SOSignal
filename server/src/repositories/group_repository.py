from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete

from models import Group, Stuff


class GroupReposiotory:
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def create(self, stuff_list: list[Stuff], order_id: int) -> None:
        values = [{"stuff_id": stuff.id, "order_id": order_id} for stuff in stuff_list]
        query = insert(Group).values(values)
        await self.__session.execute(query)
        await self.__session.commit()

    async def delete(self) -> ...:
        ...
    
