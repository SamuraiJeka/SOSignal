from pydantic import BaseModel, Field, field_validator, PositiveInt

from models.user_model import TypeProblemEnum


class UserPostSchema(BaseModel):
    full_name: str
    email: str
    password: str
    problem_type: str

    @field_validator("problem_type")
    def validate_problem_type(cls, problem: str) -> str:
        values = {item.name for item in TypeProblemEnum}
        if problem not in values:
            raise ValueError(
                f"Invalid problem_type. Allowed values: {values}"
            )
        return problem


class UserSchema(BaseModel):
    id: PositiveInt
    full_name: str
    email: str
    problem_type: str


class UserPatchSchema(BaseModel):
    full_name: str | None = Field(default=None)
    email: str | None = Field(default=None)
    password: str | None = Field(default=None)
    problem_type: str | None = Field(default=None)

    @field_validator("problem_type")
    def validate_problem_type(cls, problem: str | None) -> str | None:
        if problem is None:
            return None
        values = {item.name for item in TypeProblemEnum}
        if problem not in values:
            raise ValueError(
                f"Invalid problem_type. Allowed values: {values}"
            )
        return problem
