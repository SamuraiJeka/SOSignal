from fastapi import status 


class TokenException(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        self.status = status.HTTP_401_UNAUTHORIZED
