from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from core.settings import settings

engine = create_engine(
    url=settings.db_url,
    echo=True
)
get_session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
