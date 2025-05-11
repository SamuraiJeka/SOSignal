from datetime import date, time
from pydantic import BaseModel, Field, field_validator, PositiveInt, ValidationInfo


    class OrderPostSchema(BaseModel):
        user_id: PositiveInt
        baggage: bool = Field(default=False)
        order_date: date
        start_time: time
        finish_time: time

    @field_validator('finish_time')
    def validate_finish_time(cls, finish_time: time, info: ValidationInfo) -> time:
        if 'start_time' in info.data and finish_time <= info.data['start_time']:
            raise ValueError('finish_time must be greater than start_time')
        return finish_time


class OrderSchema(BaseModel):
    id: PositiveInt
    user_id: PositiveInt
    baggage: bool
    order_date: date
    start_time: time
    finish_time: time
