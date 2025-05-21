from typing import Annotated
from datetime import date, time
from pydantic import BaseModel, field_validator, ValidationInfo
from pydantic.functional_validators import AfterValidator
from pydantic_core import PydanticCustomError


def parse_any_time_format(v: str | time) -> time:
    if isinstance(v, time):
        return v
    
    try:
        cleaned = ''.join(c for c in v if c.isdigit() or c == ':')
        parts = cleaned.split(':')
        if len(parts) == 1:
            time_str = parts[0].zfill(4)
            hours = int(time_str[:2])
            minutes = int(time_str[2:4])
        else:
            hours = int(parts[0])
            minutes = int(parts[1]) if len(parts) > 1 else 0
        
        return time(hour=hours, minute=minutes)
    
    except (ValueError, IndexError):
        raise PydanticCustomError(
            "invalid_time_format",
            "Time must be in H:MM, HH:MM, HHMM or similar format",
            {"input": v}
        )


FlexibleTime = Annotated[time, AfterValidator(parse_any_time_format)]


class OrderPostSchema(BaseModel):
    baggage: bool = False
    order_date: date
    start_time: FlexibleTime
    finish_time: FlexibleTime

    @field_validator('finish_time')
    def validate_finish_time(cls, v: time, info: ValidationInfo) -> time:
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError("Время окончания заявки должно быть больше времени начала")
        if info.data['start_time'] == v:
            raise ValueError("Время начала заявки совподает с временем окончания")
        return v

    class Config:
        json_encoders = {
            time: lambda t: t.strftime("%H:%M"),
        }


class OrderSchema(OrderPostSchema):
    id: int
    user_id: int
