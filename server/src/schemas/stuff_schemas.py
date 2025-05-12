from pydantic import BaseModel, EmailStr


class StuffSchema(BaseModel):
    full_name: str
    email: EmailStr
