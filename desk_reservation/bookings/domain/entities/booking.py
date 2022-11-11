from datetime import datetime

import pydantic


class Booking(pydantic.BaseModel):
    booking_id: str
    office_id: str
    booked_date_init: datetime
    booked_date_end: datetime
    created_at: datetime = None
    updated_at: datetime = None
    updated_by: str = None
    deleted_at: datetime = None
    deleted_by: str = None

    @pydantic.validator('created_at', pre=True, always=True)
    @classmethod
    def default_created(cls, value):
        return value or datetime.now()


class SeatBooking(Booking):
    booked_by: dict
    desk_id: str
    seat_id: str
    has_pet: bool
    has_child: bool

class SeatBookingResponse(SeatBooking):
    seat: dict = None
    office: dict = None


class ParkingBooking(Booking):
    booked_by: dict
    parking_id: str

class LockBooking(Booking):
    locked_by: dict
    desk_id: str
    seat_id: str
