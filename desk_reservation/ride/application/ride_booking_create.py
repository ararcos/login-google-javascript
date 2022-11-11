from typing import Optional
import uuid

from ...shared.domain.exceptions import BadRequestError
from ..domain.services.ride_service import RideService
from ..domain import Ride, RideBooking


class RideBookingCreator:
    def __init__(self, ride_service: RideService):
        self.ride_service = ride_service

    def execute(self, ride_booking: RideBooking, extra_seats: int) -> Optional[Ride]:
        ride = self.ride_service.find_by_id(ride_id=ride_booking.ride_id)
        if ride:
            total_seats = len(ride.passengers) + extra_seats + 1
            if total_seats > ride.total_spots:
                raise BadRequestError("There are not enough spots available")
            result = self.ride_service.booking_ride(ride_booking=ride_booking, ride=ride)
            ride.passengers.append(result.__dict__)
            if extra_seats > 0:
                for _ in range(extra_seats):
                    update_fields = {'ride_booking_id': str(uuid.uuid4()),'has_child': False, 'has_pet': False, 'is_extra_seat': True}
                    ride_booking_extra = ride_booking.copy(update=update_fields)
                    result=self.ride_service.booking_ride(
                        ride_booking=ride_booking_extra,
                        ride=ride
                        )
                    ride.passengers.append(result.__dict__)
        return ride
