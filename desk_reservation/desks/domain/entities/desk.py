from typing import List
from datetime import datetime
import pydantic


class Desk(pydantic.BaseModel):
    desk_id: str
    desk_name: str
    top_pixel: float
    left_pixel: float
    width: float
    height: float
    seats_list: List[str]
    office_id: str
    created_at: datetime = None
    updated_at: datetime = None
    updated_by: str = None
    deleted_at: datetime = None
    deleted_by: str = None

    @pydantic.validator("created_at", pre=True, always=True)
    @classmethod
    def default_created(cls, value):
        return value or datetime.now()
