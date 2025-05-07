from sqlalchemy.orm import Session

from repositories.order_repository import OrderRepository
from repositories.user_repository import UserRepository
from schemas.order_schemas import OrderPostSchema, OrderSchema
from exceptions.user_excptions import UserNotFound


#TODO: Интегрировать сервис группы. Написать логику распределения персонала по заявкам.
class OrderService:
    def __init__(self, session: Session):
        self.__repository = OrderRepository(session)
        self.__user_repository = UserRepository(session)
    
    def create(self, order_dto: OrderPostSchema) -> OrderSchema:
        if not self.__user_repository.is_exists(id=order_dto.user_id):
            raise UserNotFound
        order = self.__repository.create(order_dto)
        return OrderSchema.model_validate(order, from_attributes=True)

    def get_by_user_id(self, user_id: int) -> list[OrderSchema]:
        if not self.__user_repository.is_exists(id=user_id):
            raise UserNotFound
        order_list = self.__repository.get_by_user_id(user_id)
        return [
            OrderSchema.model_validate(order, from_attributes=True) for order in order_list
        ]

    def delete(self, order_id: int) -> bool | None:
        result = self.__repository.delete(order_id)
        return result
