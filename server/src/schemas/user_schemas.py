from pydantic import BaseModel, Field, field_validator, PositiveInt, EmailStr

from models.user_model import TypeProblemEnum


class BaseUserSchema(BaseModel):
    @field_validator("problem_type", check_fields=False)
    def validate_problem_type(cls, problem: str) -> str | None:
        values = {item.name for item in TypeProblemEnum}
        if problem not in values:
            raise ValueError(
                f"Invalid problem_type. Allowed values: {values}"
            )
        return problem


class UserPostSchema(BaseUserSchema):
    full_name: str
    email: EmailStr
    password: str
    problem_type: str


class UserSchema(BaseModel):
    id: PositiveInt
    full_name: str
    email: EmailStr
    problem_type: str


class UserPatchSchema(BaseUserSchema):
    full_name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None)
    problem_type: str | None = Field(default=None)

    @field_validator("problem_type")
    def validate_problem_type(cls, problem: str | None) -> str | None:
        if problem is None:
            return None
        return super().validate_problem_type(problem)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str
