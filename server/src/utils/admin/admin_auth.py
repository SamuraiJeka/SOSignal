from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy import select

from models.admin_model import Admin
from core.database import get_session


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form["username"]
        password = str(form["password"])
        async with get_session() as session:
            query = select(Admin).where(Admin.name == username)
            result = await session.execute(query)
            admin = result.scalars().first()
        if admin and admin.check_password(password):
            request.session.update({"token": username})
            return True
        return False 
    
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
    
    async def authenticate(self, request: Request) -> bool:
        session_id = request.session.get("token")
        if not session_id:
            return False
        return True
