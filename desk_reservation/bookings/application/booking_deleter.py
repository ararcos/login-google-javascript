from ..domain.services import BookingService


class BookingDeleter:
    def __init__(self, booking_service: BookingService):
        self.booking_service = booking_service

    def execute(self, booking_id: str, user_id: str) -> bool:
        return self.booking_service.delete_booking(
                booking_id=booking_id,
                user_id=user_id
            )
