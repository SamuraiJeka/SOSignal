from typing import TYPE_CHECKING
from datetime import date, time
from sqlalchemy import Integer, ForeignKey, Boolean, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
if TYPE_CHECKING:
    from models import Group, User


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=False
    )
    baggage: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        unique=False
    )
    order_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        unique=True
    )
    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
        unique=False
    )
    finish_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
        unique=False
    )

    group: Mapped["Group"] = relationship("Group", back_populates="order")
    user: Mapped["User"] = relationship("User", back_populates="orders")
