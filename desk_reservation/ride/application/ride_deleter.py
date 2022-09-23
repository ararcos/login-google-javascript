from ..domain.services.ride_service import RideService


class RideDeleter:
    def __init__(self, ride_service: RideService):
        self.ride_service = ride_service

    def execute(self, user_id: str, ride_id: str) -> bool:
        return self.ride_service.delete(user_id=user_id, ride_id=ride_id)
