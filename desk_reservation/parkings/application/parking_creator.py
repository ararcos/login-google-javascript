from ..domain.entities.parking import Parking
from ..domain.services.parking_service import ParkingService
from ...users.domain.entities.user import User



class ParkingCreator:
    def __init__(self, parking_service: ParkingService):
        self.parking_service = parking_service

    def execute(self, parking: Parking, user_id: str) -> Parking:
        return self.parking_service.create_parking(user_id=user_id, parking=parking)
