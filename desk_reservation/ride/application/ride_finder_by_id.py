from typing import Optional

from ..domain.entities.ride import RideResponse
from ..domain.services.ride_service import RideService

class RideFinderById:
    def __init__(self, ride_service: RideService):
        self.ride_service = ride_service

    def execute(self, ride_id: str) -> Optional[RideResponse]:
        ride = self.ride_service.find_by_id(ride_id=ride_id)
        if ride:
            user_info = self.ride_service.populate_user_info(
                offerer_user_id=ride.offerer_user_id)
            return RideResponse(rideInfo=ride, userInfo=user_info.__dict__)
        return None
