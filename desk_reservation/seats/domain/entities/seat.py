from datetime import datetime
from typing import List
import pydantic


class Seat(pydantic.BaseModel):

    seat_id: str
    desk_id: str
    office_id: str
    name: str
    deleted_at: datetime = None
    created_at: datetime = None
    is_laptop: bool
    position: List[int]
    leftPixels: float
    topPixels: float

    @pydantic.validator("created_at", pre=True, always=True)
    @classmethod
    def default_created(cls, value):
        return value or datetime.now()
