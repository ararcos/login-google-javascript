from ..domain import Ride
from ..domain.services.ride_service import RideService


class RideCreator:
    def __init__(self, ride_service: RideService):
        self.ride_service = ride_service

    def execute(self, ride_candidate: Ride) -> Ride:
        return self.ride_service.create(ride=ride_candidate)
