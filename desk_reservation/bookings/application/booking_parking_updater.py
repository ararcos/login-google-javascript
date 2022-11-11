from typing import Optional
from desk_reservation.bookings.domain.services.booking_parking_service import BookingParkingService
from ...bookings.domain.entities import SeatBooking


class BookingParkingUpdater:
    def __init__(self, booking_parking_service: BookingParkingService):
        self.booking_parking_service = booking_parking_service

    def execute(self, booking_id: str, user_id: str, booking: SeatBooking) -> Optional[SeatBooking]:
        return self.booking_parking_service.update_parking_booking(
                booking_id=booking_id,
                user_id=user_id,
                booking=booking
            )
