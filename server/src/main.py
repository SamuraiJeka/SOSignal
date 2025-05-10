import asyncio
import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from core.settings import settings
from core.database import engine
from utils.admin.admin_auth import AdminAuth
from utils.admin.views import (
    AdminView,
    UserView,
    StuffView,
    OrderView,
    GroupView
)
from routers.user_router import router as user_router
from routers.order_router import router as order_router
from routers.auth_router import router as auth_router


app = FastAPI()

authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend
)
admin.add_view(AdminView)
admin.add_view(UserView)
admin.add_view(StuffView)
admin.add_view(OrderView)
admin.add_view(GroupView)

app.include_router(user_router)
app.include_router(order_router)
app.include_router(auth_router)
