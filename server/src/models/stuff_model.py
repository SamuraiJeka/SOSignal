from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
if TYPE_CHECKING:
    from models.group_model import Group


class Stuff(Base):
    __tablename__ = "stuff"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    full_name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        unique=False
    )
    email: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=False
    )

    groups: Mapped[list["Group"]] = relationship("Group", back_populates="stuff")
