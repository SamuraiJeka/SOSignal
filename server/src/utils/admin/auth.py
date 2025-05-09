from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy import select

from models.admin import Admin
from core.database import get_session

#TODO: доделать логику аутентификации
class AdminAuth(AuthenticationBackend):
    def login_sync(self, request: Request) -> bool:
        form = request.form()
        username = form["username"]
        password = form["password"]
        with get_session() as session:
            query = select(Admin).where(Admin.name == username)
            result = session.execute(query)
            admin = result.scalars().first()
        if admin and admin.check_password(password):
            request.session.update({"token": username})
            return True
        return False 
    
    def logout_sync(self, request: Request) -> bool:
        request.session.clear()
        return True
    
    def authenticate_sync(self, request: Request) -> bool:
        return bool(request.session.get("token"))

    async def _async_wrapper(self, func, request):
        """Обертка для совместимости с async интерфейсом SQLAdmin"""
        return func(request)
    
    async def login(self, request: Request) -> bool:
        return await self._async_wrapper(self.login_sync, request)
    
    async def logout(self, request: Request) -> bool:
        return await self._async_wrapper(self.logout_sync, request)
    
    async def authenticate(self, request: Request) -> bool:
        return await self._async_wrapper(self.authenticate_sync, request)
