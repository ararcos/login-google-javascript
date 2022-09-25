from ..domain.services import BookingService
from ...bookings.domain.entities import SeatBooking


class BookingCreator:
    def __init__(self, booking_service: BookingService):
        self.booking_service = booking_service

    def execute(self, booking: SeatBooking) -> SeatBooking:
        return self.booking_service.create_booking(booking)
