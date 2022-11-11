from typing import List

from ...shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ..domain.entities import Booking
from ..domain.services import BookingService


class BookingFinder:
    def __init__(self, booking_service: BookingService):
        self.booking_service = booking_service
    def execute(self, criteria: Criteria, populate: bool) -> List[Booking]:
        return self.booking_service.find_bookings(criteria, populate)
