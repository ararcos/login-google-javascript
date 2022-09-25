from typing import Optional
from ..domain.services import BookingService
from ...bookings.domain.entities import SeatBooking


class BookingGetter:
    def __init__(self, booking_service: BookingService):
        self.booking_service = booking_service

    def execute(self, booking_id: str) -> Optional[SeatBooking]:
        return self.booking_service.get_booking_by_id(booking_id=booking_id)
