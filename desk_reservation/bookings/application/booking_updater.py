from typing import Optional
from ..domain.services import BookingService
from ...bookings.domain.entities import SeatBooking


class BookingUpdater:
    def __init__(self, booking_service: BookingService):
        self.booking_service = booking_service

    def execute(self, booking_id: str, user_id: str, booking: SeatBooking) -> Optional[SeatBooking]:
        return self.booking_service.update_booking(
                booking_id=booking_id,
                user_id=user_id,
                booking=booking
            )
