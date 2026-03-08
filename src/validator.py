"""
Validation layer
"""

import re
from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict, model_validator

class MessageData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    name: str
    mobile: str
    message: str
    schedule: str
    category: str
    status: str = ""
    compliance_flag: str = ""

    @model_validator(mode='before')
    @classmethod
    def convert_before_parse(cls, data):
        # Convert mobile number to string if it's an integer
        if isinstance(data, dict) and isinstance(data.get('mobile'), (int, float)):
            data['mobile'] = str(int(data['mobile']))
        return data

    @field_validator('mobile')
    @classmethod
    def validate_mobile(cls, v):
        if not re.match(r'^\+?\d{10,15}$', v):
            raise ValueError('Invalid mobile number')
        return v

    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if not str(v).strip():
            raise ValueError('Message cannot be empty')
        return v

    @field_validator('schedule')
    @classmethod
    def validate_schedule(cls, v):
        # Try multiple date formats
        formats = ['%Y-%m-%d %H:%M', '%d-%m-%Y %H:%M', '%Y/%m/%d %H:%M']
        dt = None
        for fmt in formats:
            try:
                dt = datetime.strptime(str(v), fmt)
                break
            except (ValueError, TypeError):
                continue
        
        if dt is None:
            raise ValueError(f'Invalid datetime format. Try YYYY-MM-DD HH:MM')
        
        if dt <= datetime.now():
            raise ValueError('Schedule must be in the future')
        return v

    @field_validator('category')
    @classmethod
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