from typing import Optional
from pydantic import BaseModel


class UserPostSchema(BaseModel):
    full_name: str
    email: str
    password: str
    problem_type: str


class UserSchema(BaseModel):
    id: int
    full_name: str
    email: str
    problem_type: str


class UserPatchSchema(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    problem_type: Optional[str] = None
