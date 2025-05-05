from enum import Enum
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


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
