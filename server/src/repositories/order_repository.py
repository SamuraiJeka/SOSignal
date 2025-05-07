from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete

from models import Order
from schemas.order_schemas import OrderPostSchema
from exceptions.order_exceptions import OrderNotFound


class OrderRepository:
    def __init__(self, session: Session):
        self.__session = session
    
    def create(self, user_dto: OrderPostSchema) -> Order | None:
        query = insert(Order).values(
            user_id=user_dto.user_id,
            baggage=user_dto.baggage,
            order_date=user_dto.order_date,
            start_time=user_dto.start_time,
            finish_time=user_dto.finish_time
        ).returning(Order)
        result = self.__session.execute(query)
        self.__session.commit()
        return result.scalar_one_or_none()
    
    def get_by_user_id(self, user_id: int) -> list[Order]:
        query = select(Order).where(Order.user_id == user_id)
        result = self.__session.execute(query)
        return list(result.scalars().all())
    
    def delete(self, order_id: int) -> bool | None:
        query = delete(Order).where(Order.id == order_id)
        result = self.__session.execute(query)
        if result.scalar() is None:
            raise OrderNotFound
        self.__session.commit()
        return bool(result)
