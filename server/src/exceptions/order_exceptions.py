from fastapi import status


class OrderNotFound(Exception):
    def __init__(self):
        self.msg = "Заявка не найдена"
        self.status = status.HTTP_404_NOT_FOUND


class OrderCreationError(Exception):
    def __init__(self):
        self.msg = "Не удалось создать заказ"
        self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
