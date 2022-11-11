

from desk_reservation.bookings.domain.services.booking_parking_service import BookingParkingService


class BookingParkingDeleter:
    def __init__(self, booking_parking_service: BookingParkingService):
        self.booking_parking_service = booking_parking_service

    def execute(self, booking_id: str, user_id: str) -> bool:
        return self.booking_parking_service.delete_parking_booking(
                booking_id=booking_id,
                user_id=user_id
            )
