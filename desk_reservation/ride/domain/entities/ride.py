from datetime import date, datetime, time
from typing import List, Union
import pydantic


class Ride(pydantic.BaseModel):
    ride_id: str
    offerer_user_id: str
    ride_date: datetime
    departure_point: str
    destiny_office: str
    destiny_latitude: float
    destiny_longitude: float
    allow_child: bool
    allow_pet: bool
    is_uber: bool
    total_spots: int
    passengers: Union[List[dict], List[str]]
    created_at: datetime = None
    updated_at: datetime = None
    updated_by: str = None
    deleted_at: datetime = None

    @pydantic.validator('created_at', pre=True, always=True)
    @classmethod
    def default_created(cls, value):
        return value or datetime.now()


class RideResponse(pydantic.BaseModel):
    rideInfo: dict
    userInfo: dict


class RideBooking(pydantic.BaseModel):
    ride_booking_id: str
    user_id: str
    ride_id: str
    user_name: str
    has_child: bool
    has_pet: bool
    user_photo: str
    is_extra_seat: bool = False
    created_at: datetime = None
    updated_at: datetime = None
    updated_by: str = None
    deleted_at: datetime = None

    @pydantic.validator('created_at', pre=True, always=True)
    @classmethod
    def default_created(cls, value):
        return value or datetime.now()
