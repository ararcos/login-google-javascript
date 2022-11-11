from typing import List
from desk_reservation.bookings.domain.entities.booking import ParkingBooking

from desk_reservation.bookings.domain.services.booking_parking_service import BookingParkingService
from ...shared.infrastructure.firestore.firestore_criteria.criteria import Criteria


class BookingParkingFinder:
    def __init__(self, booking_parking_service: BookingParkingService):
        self.booking_parking_service = booking_parking_service
    def execute(self, criteria: Criteria) -> List[ParkingBooking]:
        return self.booking_parking_service.find_parking_bookings(criteria)
