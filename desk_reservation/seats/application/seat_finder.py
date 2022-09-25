from typing import List

from ..domain.services.seat_service import SeatService
from ...shared.infrastructure.firestore.firestore_criteria.criteria import Criteria

from ..domain import Seat


class SeatFinder:
    def __init__(self, seat_service: SeatService):
        self.seat_service = seat_service

    def execute(self,  criteria: Criteria) -> List[Seat]:
        return self.seat_service.find_seats(criteria)
