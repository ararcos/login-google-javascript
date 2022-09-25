from ..domain.services.parking_service import ParkingService
from ...users.domain.entities.user import User



class ParkingDeleter:
    def __init__(self, parking_service: ParkingService):
        self.parking_service = parking_service

    def execute(self, parking_id: str, office_id: str, user: User) -> bool:
        return self.parking_service.delete_parking(
            user_id=user.google_id, parking_id=parking_id, office_id=office_id)
