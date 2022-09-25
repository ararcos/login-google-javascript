from typing import List

from ..domain.entities.parking import Parking
from ..domain.services.parking_service import ParkingService
from ...shared.infrastructure.firestore.firestore_criteria.criteria import Criteria


class ParkingFinder:
    def __init__(self, parking_service: ParkingService):
        self.parking_service = parking_service

    def execute(self, criteria: Criteria) -> List[Parking]:
        return self.parking_service.find_parkings(criteria=criteria)
