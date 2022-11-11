from datetime import datetime
from typing import List, Union
import pydantic

class Office(pydantic.BaseModel):
    office_id: str
    name: str
    managers: List[str]
    desks: List[str]
    seats: Union[List[str], List[dict]]
    parkings: Union[List[str], List[dict]]
    floor_image: str = None
    created_at: datetime = None
    updated_at: datetime = None
    updated_by: str = None
    deleted_at: datetime = None
    deleted_by: str = None

    @pydantic.validator('created_at', pre=True, always=True)
    @classmethod
    def default_created(cls, value):
        return value or datetime.now()
