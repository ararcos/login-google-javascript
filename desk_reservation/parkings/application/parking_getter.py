from ..domain.entities.parking import Parking
from ..domain.services.parking_service import ParkingService



class ParkingGetter:
    def __init__(self, parking_service: ParkingService):
        self.parking_service = parking_service

    def execute(self, parking_id: str) -> Parking:
        return self.parking_service.get_parking_by_id(parking_id=parking_id)
