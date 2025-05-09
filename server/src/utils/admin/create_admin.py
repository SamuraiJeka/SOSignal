import asyncio
import random
import string

from core.database import get_session
from models.admin_model import Admin


def random_password():
    characters = string.ascii_letters + string.digits

    random_password = "".join(random.choices(characters, k=8))
    return random_password


async def create_admin() -> None:
    async with get_session() as session:
        password = random_password()
        admin = Admin(name="admin", password=password)
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        print(f"-\nПароль: {password}\n-")


if __name__ == "__main__":
    asyncio.run(create_admin())
