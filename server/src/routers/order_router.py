from fastapi import APIRouter, HTTPException, Depends

from core.database import get_session
from schemas.order_schemas import OrderPostSchema, OrderSchema
from schemas.user_schemas import UserSchema
from schemas.stuff_schemas import StuffSchema
from services.order_service import OrderService
from exceptions.order_exceptions import OrderNotFound, OrderCreationError
from exceptions.user_excptions import UserNotFound
from exceptions.stuff_exceptions import Understaffed, StuffNotFound
from utils.auth import get_current_user


router = APIRouter(prefix="/order", tags=["order"])


@router.post("/")
async def post_order(
    order_dto: OrderPostSchema,
    current_user: UserSchema = Depends(get_current_user)
) -> OrderSchema:
    try:
        async with get_session() as session:
            return await OrderService(session).create(current_user.id, order_dto)
    except UserNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)
    except Understaffed as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)
    except StuffNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)
    except OrderCreationError as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)


@router.get("/user")
async def get_by_user_id(
    current_user: UserSchema = Depends(get_current_user)
) -> list[OrderSchema]:
    try:
        async with get_session() as session:
            return await OrderService(session).get_by_user_id(current_user.id)
    except UserNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)


@router.delete("/{id}")
async def delete(
    id: int,
    current_user: UserSchema = Depends(get_current_user)
) -> bool | None:
    try:
        async with get_session() as session:
            return await OrderService(session).delete(id)
    except OrderNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)


@router.get("/stuff/{id}")
async def get_stuff(
    id: int,
    current_user: UserSchema = Depends(get_current_user)
) -> list[StuffSchema]:
    try:
        async with get_session() as session:
            return await OrderService(session).get_stuff_by_id(id)
    except StuffNotFound as exc:
        raise HTTPException(detail=exc.msg, status_code=exc.status)
