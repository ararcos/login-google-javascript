
from desk_reservation.bookings.domain.entities.booking import ParkingBooking
from desk_reservation.bookings.domain.services.booking_parking_service import BookingParkingService

class BookingParkingCreator:
    def __init__(self, booking_parking_service: BookingParkingService):
        self.booking_parking_service = booking_parking_service

    def execute(self, booking: ParkingBooking) -> ParkingBooking:
        return self.booking_parking_service.create_parking_booking(booking)
