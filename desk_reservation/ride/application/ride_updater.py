from typing import Optional

from ..domain.services.ride_service import RideService
from ..domain import Ride


class RideUpdater:
    def __init__(self, ride_service: RideService):
        self.ride_service = ride_service

    def execute(self, user_id: str, ride_id, edited_ride: Ride) -> Optional[Ride]:
        return self.ride_service.update(
            user_id=user_id, ride=edited_ride, ride_id=ride_id
        )
