from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class ErrorResponse(BaseModel):
    detail: str

class Comment(BaseModel):
    comment_id: int
    text: str
    polarity_score: float
    sentiment: str

class Inputs(BaseModel):
    subfeddit_name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    sort_by_polarity: Optional[bool] = False

    @validator('start_date', 'end_date', pre=True, always=False)
    def validate_date_format(cls, value):
        if value is None:
            return value
        try:
            dt = datetime.strptime(value, '%d-%m-%Y').date()
            dt_obj = datetime.combine(dt, datetime.min.time())
            return str(dt_obj.timestamp())
        except ValueError:
            raise ValueError('Date must be in MM-DD-YYYY format')

    @validator('end_date')
    def check_date_order(cls, end_date, values):
        start_date = values.get('start_date')
        if start_date and end_date and end_date < start_date:
            raise ValueError('end_date must be after start_date')
        return end_date 