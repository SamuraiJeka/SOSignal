from fastapi import status


class UserNotFound(Exception):
    def __init__(self):
        self.msg = "Пользователь не найден"
        self.status = status.HTTP_404_NOT_FOUND


class UserAlreadyExist(Exception):
    def __init__(self, email: str):
        self.msg = f"Пользователь с почтой {email} уже существует"
        self.status = status.HTTP_400_BAD_REQUEST


class UserListIsEmpty(Exception):
    def __init__(self):
        self.msg = "Список пользователей пустой"
        self.status = status.HTTP_400_BAD_REQUEST
