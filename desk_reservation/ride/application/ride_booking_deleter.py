from ..domain.services.ride_service import RideService
from typing import List

class RideBookingDeleter:
    def __init__(self, ride_service: RideService):
        self.ride_service = ride_service

    def execute(self, ride_id: str, ride_booking_ids: List[str]) -> bool:
        return self.ride_service.delete_booking_ride(ride_id=ride_id, ride_booking_ids=ride_booking_ids)
