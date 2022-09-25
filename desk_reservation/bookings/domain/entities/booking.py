from datetime import datetime

import pydantic


class Booking(pydantic.BaseModel):
    booking_id: str
    office_id: str
    booked_by: dict
    booked_date_init: datetime
    booked_date_end: datetime
    created_at: datetime = None
    updated_at: datetime = None
    updated_by: str = None
    deleted_at: datetime = None
    deleted_by: str = None

    @pydantic.validator('created_at', pre=True, always=True)
    def default_created(cls, v):
        return v or datetime.now()


class SeatBooking(Booking):
    desk_id: str
    seat_id: str
    has_pet: bool
    has_child: bool


class ParkingBooking(Booking):
    parking_id: str
    floor: str
    name: str
