from typing import TYPE_CHECKING
from enum import Enum
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
if TYPE_CHECKING:
    from models import Order


class TypeProblemEnum(Enum):
    BLINDNESS = "проблемы со зрением"
    WHEELCHAIR = "коляска"


class User(Base):
    __tablename__ = "users"

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
    problem_type: Mapped[TypeProblemEnum] = mapped_column(
        nullable=False,
        unique=False
    )

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
