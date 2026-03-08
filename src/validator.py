"""
Validation layer
"""

import re
from datetime import datetime
from pydantic import BaseModel, validator

class MessageData(BaseModel):
    name: str
    mobile: str
    message: str
    schedule: str
    category: str
    status: str = ""
    compliance_flag: str = ""

    @validator('mobile')
    def validate_mobile(cls, v):
        if not re.match(r'^\+?\d{10,15}$', v):
            raise ValueError('Invalid mobile number')
        return v

    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v

    @validator('schedule')
    def validate_schedule(cls, v):
        try:
            dt = datetime.strptime(v, '%Y-%m-%d %H:%M')
            if dt <= datetime.now():
                raise ValueError('Schedule must be in the future')
        except ValueError:
            raise ValueError('Invalid datetime format')
        return v

    @validator('category')
    def validate_category(cls, v):
        allowed = ['Performance Update', 'Research Insight', 'Product Communication', 'Marketing']
        if v not in allowed:
            raise ValueError('Invalid category')
        return v

def validate_row(row):
    try:
        MessageData(**row)
        return True, ""
    except Exception as e:
        return False, str(e)