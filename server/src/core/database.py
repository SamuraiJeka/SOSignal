from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from core.settings import settings


engine = create_async_engine(url=settings.db_url, echo=True)
get_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
