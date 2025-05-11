from fastapi import status


class StuffNotFound(Exception):
    def __init__(self):
        self.msg = "Работники не найдены"
        self.status = status.HTTP_404_NOT_FOUND


class Understaffed(Exception):
    def __init__(self):
        self.msg = "Работников не хватает"
        self.status = status.HTTP_503_SERVICE_UNAVAILABLE