from pydantic import BaseModel, validator
from typing import List, Optional

class Build(BaseModel):
    cpu: Optional[int] = None
    gpu: Optional[int] = None
    mb: Optional[int] = None
    ram: Optional[int] = None
    storage: Optional[int] = None
    colling: Optional[int] = None
    case: Optional[int] = None
    psu: Optional[int] = None

    @validator('*', pre=True)
    def convert_empty_string_to_none(cls, value):
        if value == '':
            return None
        return value
    
    
