import bcrypt
from sqlalchemy import Integer, String, event
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), unique=False, nullable=False)

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password.encode())
    
    def set_password(self, password: str) -> None:
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


@event.listens_for(Admin, "before_insert")
@event.listens_for(Admin, "before_update")
def hash_password(mapper, connection, target):
    if target.password and not target.password.startswith("$2b$"):
        target.set_password(target.password)
