import uvicorn
from fastapi import FastAPI

from routers.user_router import router as user_router
from routers.order_router import router as order_router


app = FastAPI()

app.include_router(user_router)
app.include_router(order_router)


if __name__ == '__main__':
    uvicorn.run(app)
