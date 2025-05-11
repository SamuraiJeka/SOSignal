from fastapi import APIRouter, HTTPException

from core.database import get_session
from schemas.order_schemas import OrderPostSchema, OrderSchema
from services.order_service import OrderService
from exceptions.order_exceptions import OrderNotFound
from exceptions.user_excptions import UserNotFound


router = APIRouter(prefix="/order", tags=["order"])


@router.post("/")
async def post_order(order_dto: OrderPostSchema) -> OrderSchema:
    try:
        async with get_session() as session:
            return await OrderService(session).create(order_dto)
    except UserNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)


@router.get("/user/{id}")
async def get_by_user_id(id: int) -> list[OrderSchema]:
    try:
        async with get_session() as session:
            return await OrderService(session).get_by_user_id(id)
    except UserNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)


@router.delete("/{id}")
async def delete(id: int) -> bool | None:
    try:
        async with get_session() as session:
            return await OrderService(session).delete(id)
    except OrderNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)
