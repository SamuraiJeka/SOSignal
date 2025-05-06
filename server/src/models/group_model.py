from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
if TYPE_CHECKING:
    from models import Order, Stuff


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=False
    )
    stuff_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("stuff.id", ondelete="CASCADE"),
        nullable=False,
        unique=False
    )

    stuff: Mapped["Stuff"] = relationship("Stuff", back_populates="groups")
    order: Mapped["Order"] = relationship("Order", back_populates="group")
