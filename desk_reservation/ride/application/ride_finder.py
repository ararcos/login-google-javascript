from typing import List

from ..domain.entities.ride import RideResponse
from ..domain.services.ride_service import RideService
from ...shared.infrastructure import Criteria


class RideFinder:
    def __init__(self, ride_service: RideService):
        self.ride_service = ride_service

    def execute(self, criteria: Criteria) -> List[RideResponse]:
        populated_rides: List[RideResponse] = []
        riders = self.ride_service.find_all(criteria=criteria)
        for ride in riders:
            populated_rides.append(
                RideResponse(
                    rideInfo=ride.__dict__,
                    userInfo=self.ride_service.populate_user_info(
                        ride.offerer_user_id
                    ).__dict__,
                )
            )
        return populated_rides
