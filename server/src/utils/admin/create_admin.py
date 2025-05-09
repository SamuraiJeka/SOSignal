import random
import string
from sqlalchemy.exc import IntegrityError

from core.database import get_session
from models.admin import Admin


def random_password():
    characters = string.ascii_letters + string.digits

    random_password = "".join(random.choices(characters, k=8))
    return random_password


def create_admin() -> None:
    with get_session() as session:
        password = random_password()
        admin = Admin(name="admin", password=password)
        try:
            session.add(admin)
            session.commit()
            session.refresh(admin)
        except IntegrityError:
            print("Админ уже создан")
            session.rollback()
        else:
            print(f"-\nПароль: {password}\n-")


if __name__ == "__main__":
    create_admin()
