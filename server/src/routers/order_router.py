from fastapi import APIRouter, HTTPException

from core.database import get_session
from schemas.order_schemas import OrderPostSchema, OrderSchema
from services.order_service import OrderService
from exceptions.order_exceptions import OrderNotFound
from exceptions.user_excptions import UserNotFound


router = APIRouter(prefix="/order", tags=["order"])


@router.post("/")
def post_order(order_dto: OrderPostSchema) -> OrderSchema:
    try:
        with get_session() as session:
            return OrderService(session).create(order_dto)
    except UserNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)


@router.get("/user/{id}")
def get_by_user_id(id: int) -> list[OrderSchema]:
    try:
        with get_session() as session:
            return OrderService(session).get_by_user_id(id)
    except UserNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)


@router.delete("/{id}")
def delete(id: int) -> bool:
    try:
        with get_session() as session:
            return OrderService(session).delete(id)
    except OrderNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)
