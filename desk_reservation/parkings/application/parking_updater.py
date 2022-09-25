from ..domain.entities.parking import Parking
from ..domain.services.parking_service import ParkingService
from ...users.domain.entities.user import User



class ParkingUpdater:
    def __init__(self, parking_service: ParkingService):
        self.parking_service = parking_service

    def execute(self, parking: Parking, user: User) -> Parking:
        return self.parking_service.update_parking(user_id=user.google_id, parking=parking)
 