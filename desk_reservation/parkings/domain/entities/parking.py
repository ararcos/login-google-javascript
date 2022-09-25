from datetime import datetime
from typing import List
import pydantic


# pylint: disable=E1101
class Parking(pydantic.BaseModel):

    parking_id: str
    office_id: str
    floor: int
    name: str
    deleted_at: datetime = None
    created_at: datetime = None
    position: List[int]

    @pydantic.validator("created_at", pre=True, always=True)
    @classmethod
    def default_created(cls, value):
        return value or datetime.now()
